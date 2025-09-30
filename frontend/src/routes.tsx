import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import ProductsPage from './pages/ProductsPage';
import UsersPage from './pages/UsersPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <ProductsPage />,
      },
      {
        path: 'products',
        element: <ProductsPage />,
      },
      {
        path: 'users',
        element: <UsersPage />,
      },
    ],
  },
]);
