"""
MikroTik API endpoints
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import MikroTikRouter, Client, Plan
from app.services.mikrotik_service import MikroTikService
from app.services.mikrotik_advanced_service import MikroTikAdvancedService
import logging

mikrotik_bp = Blueprint('mikrotik', __name__)
logger = logging.getLogger(__name__)

@mikrotik_bp.route('/routers', methods=['GET'])
@jwt_required()
def get_routers():
    """Get all MikroTik routers"""
    try:
        routers = MikroTikRouter.query.all()
        return jsonify({
            'success': True,
            'routers': [r.to_dict() for r in routers]
        }), 200
    except Exception as e:
        logger.error(f"Error getting routers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/routers/<router_id>', methods=['GET'])
@jwt_required()
def get_router(router_id):
    """Get specific router details"""
    try:
        router = MikroTikRouter.query.get(router_id)
        if not router:
            return jsonify({'success': False, 'error': 'Router not found'}), 404
        
        # Connect and get detailed info
        service = MikroTikService(router_id)
        if not service.api:
            return jsonify({'success': False, 'error': 'Could not connect to router'}), 500
        
        router_info = service.get_router_info()
        interface_stats = service.get_interface_stats()
        
        return jsonify({
            'success': True,
            'router': router.to_dict(),
            'info': router_info,
            'interfaces': interface_stats
        }), 200
    except Exception as e:
        logger.error(f"Error getting router {router_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/provision', methods=['POST'])
@jwt_required()
def provision_client():
    """Provision a new client on MikroTik"""
    try:
        data = request.get_json()
        client_id = data.get('client_id')
        router_id = data.get('router_id')
        
        if not client_id or not router_id:
            return jsonify({'success': False, 'error': 'Missing client_id or router_id'}), 400
        
        client = Client.query.get(client_id)
        router = MikroTikRouter.query.get(router_id)
        
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        if not router:
            return jsonify({'success': False, 'error': 'Router not found'}), 404
        
        # Provision client
        service = MikroTikService(router_id)
        results = service.provision_client(client, client.plan, data.get('config', {}))
        
        if results['success']:
            client.status = 'active'
            from app import db
            db.session.commit()
        
        return jsonify(results), 200 if results['success'] else 500
    except Exception as e:
        logger.error(f"Error provisioning client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/clients/<client_id>/suspend', methods=['POST'])
@jwt_required()
def suspend_client(client_id):
    """Suspend client access"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'non-payment')
        
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Find router for this client
        router = MikroTikRouter.query.filter_by(isp_id=client.isp_id, is_active=True).first()
        if not router:
            return jsonify({'success': False, 'error': 'No active router found'}), 404
        
        service = MikroTikService(router.id)
        success = service.suspend_client(client, reason)
        
        if success:
            client.status = 'suspended'
            from app import db
            db.session.commit()
            return jsonify({'success': True, 'message': f'Client suspended: {reason}'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to suspend client'}), 500
    except Exception as e:
        logger.error(f"Error suspending client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/clients/<client_id>/activate', methods=['POST'])
@jwt_required()
def activate_client(client_id):
    """Activate suspended client"""
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        router = MikroTikRouter.query.filter_by(isp_id=client.isp_id, is_active=True).first()
        if not router:
            return jsonify({'success': False, 'error': 'No active router found'}), 404
        
        service = MikroTikService(router.id)
        success = service.activate_client(client)
        
        if success:
            client.status = 'active'
            from app import db
            db.session.commit()
            return jsonify({'success': True, 'message': 'Client activated'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to activate client'}), 500
    except Exception as e:
        logger.error(f"Error activating client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/clients/<client_id>/update-speed', methods=['POST'])
@jwt_required()
def update_client_speed(client_id):
    """Update client speed/plan"""
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        new_plan = Plan.query.get(plan_id)
        if not new_plan:
            return jsonify({'success': False, 'error': 'Plan not found'}), 404
        
        router = MikroTikRouter.query.filter_by(isp_id=client.isp_id, is_active=True).first()
        if not router:
            return jsonify({'success': False, 'error': 'No active router found'}), 404
        
        service = MikroTikService(router.id)
        success = service.update_client_speed(client, new_plan)
        
        if success:
            client.plan_id = plan_id
            from app import db
            db.session.commit()
            return jsonify({'success': True, 'message': f'Speed updated to {new_plan.name}'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to update speed'}), 500
    except Exception as e:
        logger.error(f"Error updating client speed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@mikrotik_bp.route('/routers/<router_id>/health', methods=['GET'])
@jwt_required()
def get_router_health(router_id):
    """Get router health status"""
    try:
        service =
