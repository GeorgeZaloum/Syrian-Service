import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { ArrowLeft, Save } from 'lucide-react';
import type { Service, ServiceFormData } from '@/types';

interface ServiceFormProps {
  service?: Service | null;
  onSubmit: (data: ServiceFormData) => void;
  onCancel: () => void;
  isSubmitting: boolean;
}

export function ServiceForm({ service, onSubmit, onCancel, isSubmitting }: ServiceFormProps) {
  const [formData, setFormData] = useState<ServiceFormData>({
    name: '',
    description: '',
    location: '',
    cost: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (service) {
      setFormData({
        name: service.name,
        description: service.description,
        location: service.location,
        cost: service.cost,
      });
    }
  }, [service]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Service name is required';
    } else if (formData.name.length < 3) {
      newErrors.name = 'Service name must be at least 3 characters';
    } else if (formData.name.length > 200) {
      newErrors.name = 'Service name must not exceed 200 characters';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    } else if (formData.description.length < 10) {
      newErrors.description = 'Description must be at least 10 characters';
    }

    if (!formData.location.trim()) {
      newErrors.location = 'Location is required';
    } else if (formData.location.length > 200) {
      newErrors.location = 'Location must not exceed 200 characters';
    }

    if (!formData.cost.trim()) {
      newErrors.cost = 'Cost is required';
    } else {
      const costValue = parseFloat(formData.cost);
      if (isNaN(costValue)) {
        newErrors.cost = 'Cost must be a valid number';
      } else if (costValue < 0) {
        newErrors.cost = 'Cost must be a positive number';
      } else if (costValue > 999999.99) {
        newErrors.cost = 'Cost must not exceed 999,999.99';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: keyof ServiceFormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="sm" onClick={onCancel} disabled={isSubmitting}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        <div>
          <h2 className="text-2xl font-bold">
            {service ? 'Edit Service' : 'Add New Service'}
          </h2>
          <p className="text-sm text-muted-foreground">
            {service ? 'Update your service details' : 'Create a new service offering'}
          </p>
        </div>
      </div>

      <Card className="p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Service Name */}
          <div className="space-y-2">
            <Label htmlFor="name">
              Service Name <span className="text-red-500">*</span>
            </Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., Home Cleaning Service"
              disabled={isSubmitting}
              className={errors.name ? 'border-red-500' : ''}
            />
            {errors.name && <p className="text-sm text-red-500">{errors.name}</p>}
            <p className="text-xs text-muted-foreground">
              {formData.name.length}/200 characters
            </p>
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">
              Description <span className="text-red-500">*</span>
            </Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Describe your service in detail..."
              rows={5}
              disabled={isSubmitting}
              className={errors.description ? 'border-red-500' : ''}
            />
            {errors.description && (
              <p className="text-sm text-red-500">{errors.description}</p>
            )}
            <p className="text-xs text-muted-foreground">
              Provide a detailed description of what your service includes
            </p>
          </div>

          {/* Location */}
          <div className="space-y-2">
            <Label htmlFor="location">
              Location <span className="text-red-500">*</span>
            </Label>
            <Input
              id="location"
              value={formData.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="e.g., New York, NY or Remote"
              disabled={isSubmitting}
              className={errors.location ? 'border-red-500' : ''}
            />
            {errors.location && <p className="text-sm text-red-500">{errors.location}</p>}
            <p className="text-xs text-muted-foreground">
              {formData.location.length}/200 characters
            </p>
          </div>

          {/* Cost */}
          <div className="space-y-2">
            <Label htmlFor="cost">
              Cost (USD) <span className="text-red-500">*</span>
            </Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground">
                $
              </span>
              <Input
                id="cost"
                type="text"
                value={formData.cost}
                onChange={(e) => handleChange('cost', e.target.value)}
                placeholder="0.00"
                disabled={isSubmitting}
                className={`pl-7 ${errors.cost ? 'border-red-500' : ''}`}
              />
            </div>
            {errors.cost && <p className="text-sm text-red-500">{errors.cost}</p>}
            <p className="text-xs text-muted-foreground">
              Enter the price for your service (e.g., 50.00)
            </p>
          </div>

          {/* Form Actions */}
          <div className="flex gap-3 pt-4 border-t">
            <Button type="submit" disabled={isSubmitting} className="flex-1">
              <Save className="h-4 w-4 mr-2" />
              {isSubmitting
                ? service
                  ? 'Updating...'
                  : 'Creating...'
                : service
                ? 'Update Service'
                : 'Create Service'}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Card>

      <Card className="p-4 bg-muted">
        <p className="text-sm text-muted-foreground">
          <strong>Note:</strong> All fields marked with <span className="text-red-500">*</span> are
          required. Your service will be visible to users immediately after creation.
        </p>
      </Card>
    </div>
  );
}
