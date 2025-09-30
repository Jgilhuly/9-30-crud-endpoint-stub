import { useState } from 'react';
import type { paths } from '../types/openapi';

type Product = paths['/products']['get']['responses']['200']['content']['application/json'][0];
type ProductCreate = paths['/products']['post']['requestBody']['content']['application/json'];
type ProductUpdate = paths['/products/{product_id}']['put']['requestBody']['content']['application/json'];

interface ProductFormProps {
  product?: Product | null;
  onSubmit: (data: ProductCreate | ProductUpdate) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export default function ProductForm({ product, onSubmit, onCancel, isLoading }: ProductFormProps) {
  const [formData, setFormData] = useState({
    name: product?.name || '',
    description: product?.description || '',
    price: product?.price || 0,
    category: product?.category || '',
    tags: product?.tags?.join(', ') || '',
    in_stock: product?.in_stock ?? true,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    if (formData.price < 0) {
      newErrors.price = 'Price must be positive';
    }
    if (!formData.category.trim()) {
      newErrors.category = 'Category is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    const tags = formData.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0);

    const submitData = {
      ...formData,
      price: Number(formData.price),
      tags,
    };

    onSubmit(submitData);
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label className="form-label" htmlFor="name">
          Name *
        </label>
        <input
          type="text"
          id="name"
          name="name"
          className="form-input"
          value={formData.name}
          onChange={handleChange}
          required
        />
        {errors.name && <div className="error">{errors.name}</div>}
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="description">
          Description *
        </label>
        <textarea
          id="description"
          name="description"
          className="form-textarea"
          value={formData.description}
          onChange={handleChange}
          required
        />
        {errors.description && <div className="error">{errors.description}</div>}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label" htmlFor="price">
            Price *
          </label>
          <input
            type="number"
            id="price"
            name="price"
            className="form-input"
            value={formData.price}
            onChange={handleChange}
            min="0"
            step="0.01"
            required
          />
          {errors.price && <div className="error">{errors.price}</div>}
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="category">
            Category *
          </label>
          <input
            type="text"
            id="category"
            name="category"
            className="form-input"
            value={formData.category}
            onChange={handleChange}
            required
          />
          {errors.category && <div className="error">{errors.category}</div>}
        </div>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="tags">
          Tags (comma-separated)
        </label>
        <input
          type="text"
          id="tags"
          name="tags"
          className="form-input"
          value={formData.tags}
          onChange={handleChange}
          placeholder="electronics, wireless, premium"
        />
      </div>

      <div className="form-group">
        <div className="checkbox-group">
          <input
            type="checkbox"
            id="in_stock"
            name="in_stock"
            className="checkbox"
            checked={formData.in_stock}
            onChange={handleChange}
          />
          <label className="form-label" htmlFor="in_stock">
            In Stock
          </label>
        </div>
      </div>

      <div className="modal-footer">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : (product ? 'Update' : 'Create')}
        </button>
      </div>
    </form>
  );
}
