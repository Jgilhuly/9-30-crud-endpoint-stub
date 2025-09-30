import { api } from './client';
import type { paths } from '../types/openapi';

type Product = paths['/products']['get']['responses']['200']['content']['application/json'][0];
type ProductCreate = paths['/products']['post']['requestBody']['content']['application/json'];
type ProductUpdate = paths['/products/{product_id}']['put']['requestBody']['content']['application/json'];

export const productsApi = {
  listProducts: async (): Promise<Product[]> => {
    const response = await api.get('/products');
    return response.data;
  },

  getProduct: async (id: number): Promise<Product> => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  createProduct: async (product: ProductCreate): Promise<Product> => {
    const response = await api.post('/products', product);
    return response.data;
  },

  updateProduct: async (id: number, product: ProductUpdate): Promise<Product> => {
    const response = await api.put(`/products/${id}`, product);
    return response.data;
  },

  deleteProduct: async (id: number): Promise<void> => {
    await api.delete(`/products/${id}`);
  },
};
