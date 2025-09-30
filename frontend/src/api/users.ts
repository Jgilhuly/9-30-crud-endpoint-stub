import { api } from './client';
import type { paths } from '../types/openapi';

type User = paths['/users']['get']['responses']['200']['content']['application/json'][0];
type UserCreate = paths['/users']['post']['requestBody']['content']['application/json'];
type UserUpdate = paths['/users/{user_id}']['put']['requestBody']['content']['application/json'];

export const usersApi = {
  listUsers: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
  },

  getUser: async (id: number): Promise<User> => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  createUser: async (user: UserCreate): Promise<User> => {
    const response = await api.post('/users', user);
    return response.data;
  },

  updateUser: async (id: number, user: UserUpdate): Promise<User> => {
    const response = await api.put(`/users/${id}`, user);
    return response.data;
  },

  deleteUser: async (id: number): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};
