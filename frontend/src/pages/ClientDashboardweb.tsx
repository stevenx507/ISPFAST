import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  WifiIcon, 
  ChartBarIcon, 
  CreditCardIcon,
  SupportIcon,
  UserGroupIcon,
  CogIcon,
  BellIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import SpeedTestWidget from '../components/SpeedTestWidget'
import BillingWidget from '../components/BillingWidget'
import SupportChat from '../components/SupportChat'
import NetworkMap from '../components/NetworkMap'

const ClientDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [notifications, setNotifications] = useState(3)
  const [serviceStatus, setServiceStatus] = useState({
    internet: 'active',
    speed: '85/20 Mbps',
    ping: '12ms',
    uptime: '99.9%'
  })

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: ChartBarIcon },
    { id: 'billing', name: 'Facturación', icon: CreditCardIcon },
    { id: 'network', name: 'Red', icon: WifiIcon },
    { id: 'support', name: 'Soporte', icon: SupportIcon },
    { id: 'profile', name: 'Perfil', icon: UserGroupIcon },
    { id: 'settings', name: 'Configuración', icon: CogIcon }
  ]

  const stats = [
    { label: 'Velocidad Actual', value: '85/20 Mbps', change: '+5%' },
    { label: 'Uso del Mes', value: '45%', change: '-2%' },
    { label: 'Próxima Factura', value: '$29.99', change: 'Vence en 15 días' },
    { label: 'Dispositivos', value: '12', change: '+2 esta semana' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">IM</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">ISPMAX</h1>
                <p className="text-sm text-gray-600">Panel del Cliente</p>
              </div>
            </div>

            {/* Status & Notifications */}
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-lg border border-green-200">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-green-700">
                  Servicio Activo
                </span>
              </div>

              <button className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg">
                <BellIcon className="w-6 h-6" />
                {notifications > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {notifications}
                  </span>
                )}
              </button>

              {/* User Menu */}
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">JP</span>
                </div>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-900">Juan Pérez</p>
                  <p className="text-xs text-gray-600">Plan: Gamer 100M</p>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex space-x-8 overflow-x-auto py-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 text-sm font-medium rounded-lg whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnimatePresence mode="wait">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Welcome Banner */}
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
                <div className="flex flex-col md:flex-row md:items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">¡Hola, Juan!</h2>
                    <p className="text-blue-100">Tu servicio está funcionando perfectamente</p>
                  </div>
                  <div className="mt-4 md:mt-0 flex items-center space-x-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold">85/20</div>
                      <div className="text-blue-100 text-sm">Mbps Actual</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold">12ms</div>
                      <div className="text-blue-100 text-sm">Ping</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white rounded-xl p-5 shadow border border-gray-200"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="text-sm text-gray-600">{stat.label}</p>
                        <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                      </div>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                        stat.change.startsWith('+') 
                          ? 'bg-green-100 text-green-800'
                          : stat.change.startsWith('-')
                          ? 'bg-red-100 text-red-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {stat.change}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Main Content Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column */}
                <div className="lg:col-span-2 space-y-6">
                  {/* Speed Test */}
                  <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Prueba de Velocidad 4K
                      </h3>
                    </div>
                    <div className="p-6">
                      <SpeedTestWidget />
                    </div>
                  </div>

                  {/* Network Map */}
                  <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Mapa de Red
                      </h3>
                    </div>
                    <div className="p-4">
                      <NetworkMap />
                    </div>
                  </div>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                  {/* Quick Actions */}
                  <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Acciones Rápidas
                      </h3>
                    </div>
                    <div className="p-4 space-y-3">
                      {[
                        { icon: '💳', label: 'Pagar Factura', color: 'green' },
                        { icon: '🔄', label: 'Reiniciar Router', color: 'blue' },
                        { icon: '📊', label: 'Ver Uso Detallado', color: 'purple' },
                        { icon: '🎁', label: 'Invitar Amigos', color: 'orange' }
                      ].map((action) => (
                        <button
                          key={action.label}
                          className="w-full flex items-center space-x-3 p-3 text-left rounded-lg hover:bg-gray-50 transition-colors"
                        >
                          <span className="text-xl">{action.icon}</span>
                          <span className="font-medium text-gray-900">{action.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Support Chat */}
                  <div className="bg-white rounded-xl shadow border border-gray-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Soporte IA 24/7
                      </h3>
                    </div>
                    <div className="p-4">
                      <SupportChat />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Billing Tab */}
          {activeTab === 'billing' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <BillingWidget />
            </motion.div>
          )}

          {/* Network Tab */}
          {activeTab === 'network' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="bg-white rounded-xl shadow border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Configuración de Red
                </h3>
                {/* Network settings content */}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  )
}

export default ClientDashboard
