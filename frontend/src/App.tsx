import { Outlet, Link, useLocation } from 'react-router-dom'

function App() {
  const location = useLocation()

  return (
    <div className="app">
      <nav className="nav">
        <h1>CRUD App</h1>
        <div className="nav-links">
          <Link 
            to="/products" 
            className={location.pathname === '/products' || location.pathname === '/' ? 'active' : ''}
          >
            Products
          </Link>
          <Link 
            to="/users" 
            className={location.pathname === '/users' ? 'active' : ''}
          >
            Users
          </Link>
        </div>
      </nav>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}

export default App