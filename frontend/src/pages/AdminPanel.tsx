import React, { useState } from 'react'
import { 
  ChartBarIcon,
  UserGroupIcon,
  CreditCardIcon,
  WifiIcon,
  CogIcon,
  BellAlertIcon,
  MapIcon,
  ServerIcon
} from '@heroicons/react/24/outline'
import AdminDashboard from '../components/AdminDashboard'
import ProfessionalDashboard from '../components/ProfessionalDashboard'

const AdminPanel: React.FC = () => {
  const [activeView, setActiveView] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const menuItems = [
    { id: 'dashboard', name: 'Dashboard', icon: ChartBarIcon },
    { id: 'clients', name: 'Clientes', icon: UserGroupIcon },
    { id: 'billing', name: 'Facturación', icon: CreditCardIcon },
    { id: 'network', name: 'Red', icon: WifiIcon },
    { id: 'monitoring', name: 'Monitoreo', icon: ServerIcon },
    { id: 'maps', name: 'Mapas', icon: MapIcon },
    { id: 'alerts', name: 'Alertas', icon: BellAlertIcon },
    { id: 'settings', name: 'Configuración', icon: CogIcon },
    { id: 'provisioning', name: 'Provisioning', icon: CogIcon }
  ]

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Sidebar for Mobile */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)}></div>
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">IM</span>
              </div>
              <div className="ml-3">
                <h1 className="text-lg font-bold text-gray-900">ISPMAX</h1>
                <p className="text-xs text-gray-600">Panel Admin</p>
              </div>
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {menuItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveView(item.id)
                    setSidebarOpen(false)
                  }}
                  className={`group flex items-center px-2 py-2 text-base font-medium rounded-md w-full ${
                    activeView === item.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <item.icon className="mr-4 h-6 w-6" />
                  {item.name}
                </button>
              ))}
            </nav>
          </div>
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0">
        <div className="flex-1 flex flex-col min-h-0 border-r border-gray-200 bg-white">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">IM</span>
              </div>
              <div className="ml-3">
                <h1 className="text-lg font-bold text-gray-900">ISPMAX</h1>
                <p className="text-xs text-gray-600">Panel Admin</p>
              </div>
            </div>
            <nav className="mt-8 flex-1 px-4 space-y-1">
              {menuItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setActiveView(item.id)}
                  className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md w-full ${
                    activeView === item.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <item.icon className="mr-3 h-5 w-5" />
                  {item.name}
                </button>
              ))}
            </nav>
          </div>
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center w-full">
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">Admin ISP</p>
                <p className="text-xs text-gray-500">admin@ispmax.com</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64 flex flex-col">
        {/* Top navbar */}
        <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
          <button
            type="button"
            className="px-4 border-r border-gray-200 text-gray-500 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <span className="sr-only">Abrir menú</span>
            {/* Hamburger icon */}
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex">
              <h2 className="text-lg font-semibold text-gray-900 my-auto">
                {menuItems.find(item => item.id === activeView)?.name}
              </h2>
            </div>
            <div className="ml-4 flex items-center lg:ml-6">
              <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg">
                <BellAlertIcon className="h-6 w-6" />
              </button>
              <div className="ml-4 flex items-center">
                <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">A</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <main className="flex-1">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {activeView === 'dashboard' && <ProfessionalDashboard />}
              {activeView === 'clients' && <ClientsManagement />}
              {activeView === 'billing' && <BillingManagement />}
              {activeView === 'provisioning' && <Provisioning />}
              {/* Add other views as needed */}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

// Example sub-components
const ClientsManagement: React.FC = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="px-6 py-4 border-b border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900">Gestión de Clientes</h3>
    </div>
    <div className="p-6">
      <p>Contenido de gestión de clientes...</p>
    </div>
  </div>
)

const BillingManagement: React.FC = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="px-6 py-4 border-b border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900">Gestión de Facturación</h3>
    </div>
    <div className="p-6">
      <p>Contenido de facturación...</p>
    </div>
  </div>
)

const Provisioning: React.FC = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="px-6 py-4 border-b border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900">Auto-Provisioning</h3>
    </div>
    <div className="p-6">
      <p>Contenido de provisioning...</p>
    </div>
  </div>
)

export default AdminPanel
