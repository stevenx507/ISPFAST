"""
Advanced MikroTik Service with v6/v7 support
"""
import routeros_api
from typing import Dict, List, Optional, Any
import logging
import re
from datetime import datetime
from app.models import Client, Plan, MikroTikRouter
from app import db

logger = logging.getLogger(__name__)

class MikroTikAdvancedService:
    """Advanced MikroTik management service"""
    
    def __init__(self, router_ip: str, username: str, password: str, port: int = 8728):
        self.connection = None
        self.api = None
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.port = port
        self.routeros_version = None
        self.capsman_supported = False
        self.connect()
    
    def connect(self) -> bool:
        """Establish connection to MikroTik router"""
        try:
            self.connection = routeros_api.RouterOsApiPool(
                host=self.router_ip,
                username=self.username,
                password=self.password,
                port=self.port,
                plaintext_login=True,
                use_ssl=False
            )
            self.api = self.connection.get_api()
            
            # Detect router info
            self._detect_router_info()
            logger.info(f"Connected to MikroTik {self.router_ip} - v{self.routeros_version}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to MikroTik: {e}")
            raise
    
    def _detect_router_info(self):
        """Detect router version and capabilities"""
        try:
            system_resource = self.api.get_resource('/system/resource')
            system_info = system_resource.get()
            
            if system_info:
                version = system_info[0].get('version', '6.0')
                self.routeros_version = self._parse_version(version)
                
                # Detect CAPsMAN support
                try:
                    capsman_check = self.api.get_resource('/caps-man')
                    capsman_check.get()
                    self.capsman_supported = True
                except:
                    self.capsman_supported = False
                    
        except Exception as e:
            logger.warning(f"Could not detect router info: {e}")
            self.routeros_version = "6.0"
    
    def _parse_version(self, version_str: str) -> str:
        """Parse RouterOS version"""
        match = re.search(r'(\d+\.\d+)', version_str)
        return match.group(1) if match else "6.0"
    
    def is_v7(self) -> bool:
        """Check if RouterOS v7+"""
        try:
            return float(self.routeros_version) >= 7.0
        except:
            return False
    
    def provision_client(self, client: Client, plan: Plan) -> Dict[str, Any]:
        """Provision a new client with advanced configuration"""
        results = {
            'success': False,
            'steps': {},
            'errors': []
        }
        
        try:
            # 1. Configure IP address
            if client.ip_address and client.connection_type == 'static':
                results['steps']['ip_config'] = self._configure_static_ip(client)
            
            # 2. Create DHCP lease if needed
            if client.mac_address:
                results['steps']['dhcp_lease'] = self._create_dhcp_lease(client)
            
            # 3. Apply advanced QoS
            results['steps']['qos'] = self._apply_advanced_qos(client, plan)
            
            # 4. Configure firewall rules
            results['steps']['firewall'] = self._configure_client_firewall(client)
            
            # 5. Set up WiFi if CPE has wireless
            results['steps']['wifi'] = self._configure_client_wifi(client)
            
            # Check if all steps were successful
            all_success = all(results['steps'].values())
            results['success'] = all_success
            
            if all_success:
                logger.info(f"Successfully provisioned client {client.full_name}")
            else:
                logger.warning(f"Partial success provisioning client {client.full_name}")
                
        except Exception as e:
            logger.error(f"Error provisioning client: {e}")
            results['errors'].append(str(e))
        
        return results
    
    def _configure_static_ip(self, client: Client) -> bool:
        """Configure static IP for client"""
        try:
            ip_api = self.api.get_resource('/ip/address')
            ip_api.add(
                address=f"{client.ip_address}/32",
                interface="bridge-local",
                comment=f"Cliente: {client.full_name}"
            )
            return True
        except Exception as e:
            logger.error(f"Error configuring static IP: {e}")
            return False
    
    def _create_dhcp_lease(self, client: Client) -> bool:
        """Create DHCP lease for client"""
        try:
            dhcp_api = self.api.get_resource('/ip/dhcp-server/lease')
            dhcp_api.add(
                address=client.ip_address,
                mac_address=client.mac_address,
                comment=f"Cliente: {client.full_name}",
                server="dhcp1",
                disabled="no"
            )
            return True
        except Exception as e:
            logger.error(f"Error creating DHCP lease: {e}")
            return False
    
    def _apply_advanced_qos(self, client: Client, plan: Plan) -> bool:
        """Apply advanced QoS configuration"""
        try:
            if self.is_v7():
                return self._apply_v7_qos(client, plan)
            else:
                return self._apply_v6_qos(client, plan)
        except Exception as e:
            logger.error(f"Error applying QoS: {e}")
            return False
    
    def _apply_v7_qos(self, client: Client, plan: Plan) -> bool:
        """Apply v7 QoS with Cake"""
        try:
            queue_api = self.api.get_resource('/queue/simple')
            
            # Configure burst if available
            burst_limit = ""
            if plan.burst_download and plan.burst_upload:
                burst_limit = f"{plan.burst_download}M/{plan.burst_upload}M"
            
            queue_api.add(
                name=f"client_{client.id}",
                target=client.ip_address,
                max_limit=f"{plan.download_speed}M/{plan.upload_speed}M",
                burst_limit=burst_limit,
                burst_threshold=f"{plan.download_speed * 0.8}M/{plan.upload_speed * 0.8}M",
                burst_time="30s",
                queue="cake",
                comment=f"Cliente: {client.full_name} - Plan: {plan.name}"
            )
            return True
        except Exception as e:
            logger.error(f"Error applying v7 QoS: {e}")
            return False
    
    def _apply_v6_qos(self, client: Client, plan: Plan) -> bool:
        """Apply v6 QoS with PCQ"""
        try:
            # Create PCQ queue types if they don't exist
            queue_type_api = self.api.get_resource('/queue/type')
            
            # Check if PCQ types exist
            existing_types = queue_type_api.get()
            pcq_download_exists = any(t.get('name') == 'PCQ_Download' for t in
