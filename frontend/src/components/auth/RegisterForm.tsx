import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { authApi } from '@/lib/api';
import { RoleSelector } from './RoleSelector';
import { PasswordStrengthIndicator } from './PasswordStrengthIndicator';
import type { UserRole } from '@/types';

const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(/[!@#$%^&*(),.?":{}|<>]/, 'Password must contain at least one special character'),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  role: z.enum(['REGULAR', 'PROVIDER']),
  service_description: z.string().optional(),
});

type RegisterFormData = z.infer<typeof registerSchema>;

export function RegisterForm() {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'REGULAR',
    service_description: '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof RegisterFormData, string>>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    // Clear error for this field
    if (errors[name as keyof RegisterFormData]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleRoleSelect = (role: UserRole) => {
    if (role === 'REGULAR' || role === 'PROVIDER') {
      setFormData((prev) => ({ ...prev, role }));
      if (errors.role) {
        setErrors((prev) => ({ ...prev, role: undefined }));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate service description for providers
    if (formData.role === 'PROVIDER' && !formData.service_description?.trim()) {
      setErrors({ service_description: 'Service description is required for providers' });
      return;
    }

    // Validate form
    const result = registerSchema.safeParse(formData);
    if (!result.success) {
      const fieldErrors: Partial<Record<keyof RegisterFormData, string>> = {};
      result.error.issues.forEach((issue) => {
        const field = issue.path[0] as keyof RegisterFormData;
        fieldErrors[field] = issue.message;
      });
      setErrors(fieldErrors);
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      await authApi.register(formData);
      
      if (formData.role === 'REGULAR') {
        // Regular users can login immediately
        toast({
          title: 'Registration successful!',
          description: 'Your account has been created. You can now login.',
        });
        navigate('/login');
      } else {
        // Service providers need approval
        toast({
          title: 'Registration submitted!',
          description: 'Your application is pending admin approval. You will receive an email once approved.',
        });
        navigate('/login');
      }
    } catch (error: any) {
      console.error('Registration error:', error);
      
      // Extract error message from various possible response formats
      let errorMessage = 'Registration failed. Please try again.';
      
      if (error.response?.data?.error) {
        // Our custom error format
        errorMessage = error.response.data.error.message;
        
        // If there are field-specific errors, show them
        if (error.response.data.error.details) {
          const details = error.response.data.error.details;
          const fieldErrors: Partial<Record<keyof RegisterFormData, string>> = {};
          
          Object.keys(details).forEach((field) => {
            const fieldKey = field as keyof RegisterFormData;
            const errorArray = details[field];
            if (Array.isArray(errorArray) && errorArray.length > 0) {
              fieldErrors[fieldKey] = errorArray[0];
            }
          });
          
          if (Object.keys(fieldErrors).length > 0) {
            setErrors(fieldErrors);
            // Use the first field error as the toast message
            const firstError = Object.values(fieldErrors)[0];
            errorMessage = firstError || errorMessage;
          }
        }
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.email?.[0]) {
        errorMessage = error.response.data.email[0];
      }
      
      toast({
        title: 'Registration failed',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Create Account</CardTitle>
        <CardDescription>Join our service marketplace platform</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <RoleSelector
            selectedRole={formData.role}
            onRoleSelect={handleRoleSelect}
          />
          {errors.role && (
            <p className="text-sm text-red-500">{errors.role}</p>
          )}

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name</Label>
              <Input
                id="first_name"
                name="first_name"
                type="text"
                placeholder="John"
                value={formData.first_name}
                onChange={handleChange}
                disabled={isLoading}
                aria-invalid={!!errors.first_name}
              />
              {errors.first_name && (
                <p className="text-sm text-red-500">{errors.first_name}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name</Label>
              <Input
                id="last_name"
                name="last_name"
                type="text"
                placeholder="Doe"
                value={formData.last_name}
                onChange={handleChange}
                disabled={isLoading}
                aria-invalid={!!errors.last_name}
              />
              {errors.last_name && (
                <p className="text-sm text-red-500">{errors.last_name}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
              disabled={isLoading}
              aria-invalid={!!errors.email}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              disabled={isLoading}
              aria-invalid={!!errors.password}
            />
            {errors.password && (
              <p className="text-sm text-red-500">{errors.password}</p>
            )}
            <PasswordStrengthIndicator password={formData.password} />
          </div>

          {formData.role === 'PROVIDER' && (
            <div className="space-y-2">
              <Label htmlFor="service_description">Service Description</Label>
              <textarea
                id="service_description"
                name="service_description"
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="Describe the services you offer..."
                value={formData.service_description}
                onChange={handleChange}
                disabled={isLoading}
                aria-invalid={!!errors.service_description}
              />
              {errors.service_description && (
                <p className="text-sm text-red-500">{errors.service_description}</p>
              )}
            </div>
          )}

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Creating account...' : 'Create Account'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
