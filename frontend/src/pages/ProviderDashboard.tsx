import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { LogOut, Inbox, Briefcase, Settings } from 'lucide-react';
import { useAuth, useToast } from '@/hooks';
import { useNavigate } from 'react-router-dom';
import { RequestInbox, ServiceManager, ServiceForm } from '@/components/provider';
import { PasswordChangeForm } from '@/components/user';
import { servicesApi, requestsApi, authApi } from '@/lib/api';
import type { Service, ServiceFormData } from '@/types';

type ViewMode = 'list' | 'add' | 'edit';

export function ProviderDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [viewMode, setViewMode] = useState<ViewMode>('list');
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [deletingServiceId, setDeletingServiceId] = useState<number | undefined>();

  // Fetch provider's services
  const { data: servicesData, isLoading: isLoadingServices } = useQuery({
    queryKey: ['provider-services'],
    queryFn: () => servicesApi.list(),
  });

  // Fetch service requests for provider
  const { data: requestsData, isLoading: isLoadingRequests } = useQuery({
    queryKey: ['provider-requests'],
    queryFn: () => requestsApi.list(),
  });

  // Create service mutation
  const createServiceMutation = useMutation({
    mutationFn: (data: ServiceFormData) => servicesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-services'] });
      toast({
        title: 'Success',
        description: 'Service created successfully!',
      });
      setViewMode('list');
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to create service. Please try again.',
        variant: 'destructive',
      });
    },
  });

  // Update service mutation
  const updateServiceMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ServiceFormData }) =>
      servicesApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-services'] });
      toast({
        title: 'Success',
        description: 'Service updated successfully!',
      });
      setViewMode('list');
      setSelectedService(null);
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to update service. Please try again.',
        variant: 'destructive',
      });
    },
  });

  // Delete service mutation
  const deleteServiceMutation = useMutation({
    mutationFn: (id: number) => servicesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-services'] });
      toast({
        title: 'Success',
        description: 'Service deleted successfully!',
      });
      setDeletingServiceId(undefined);
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description:
          error.response?.data?.error?.message ||
          'Failed to delete service. Services with pending requests cannot be deleted.',
        variant: 'destructive',
      });
      setDeletingServiceId(undefined);
    },
  });

  // Accept request mutation
  const acceptRequestMutation = useMutation({
    mutationFn: (id: number) => requestsApi.accept(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-requests'] });
      toast({
        title: 'Success',
        description: 'Service request accepted! The user has been notified.',
      });
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to accept request. Please try again.',
        variant: 'destructive',
      });
    },
  });

  // Reject request mutation
  const rejectRequestMutation = useMutation({
    mutationFn: (id: number) => requestsApi.reject(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-requests'] });
      toast({
        title: 'Success',
        description: 'Service request rejected. The user has been notified.',
      });
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to reject request. Please try again.',
        variant: 'destructive',
      });
    },
  });

  // Change password mutation
  const changePasswordMutation = useMutation({
    mutationFn: ({ currentPassword, newPassword }: { currentPassword: string; newPassword: string }) =>
      authApi.changePassword({ current_password: currentPassword, new_password: newPassword }),
    onSuccess: () => {
      toast({
        title: 'Success',
        description: 'Password changed successfully. Please log in again.',
      });
      setTimeout(() => {
        logout();
        navigate('/login');
      }, 2000);
    },
    onError: (error: any) => {
      toast({
        title: 'Error',
        description:
          error.response?.data?.error?.message ||
          'Failed to change password. Please check your current password.',
        variant: 'destructive',
      });
    },
  });

  const handleAddService = () => {
    setSelectedService(null);
    setViewMode('add');
  };

  const handleEditService = (service: Service) => {
    setSelectedService(service);
    setViewMode('edit');
  };

  const handleDeleteService = (id: number) => {
    setDeletingServiceId(id);
    deleteServiceMutation.mutate(id);
  };

  const handleSubmitService = (data: ServiceFormData) => {
    if (viewMode === 'edit' && selectedService) {
      updateServiceMutation.mutate({ id: selectedService.id, data });
    } else {
      createServiceMutation.mutate(data);
    }
  };

  const handleCancelForm = () => {
    setViewMode('list');
    setSelectedService(null);
  };

  const handleAcceptRequest = (id: number) => {
    acceptRequestMutation.mutate(id);
  };

  const handleRejectRequest = (id: number) => {
    rejectRequestMutation.mutate(id);
  };

  const handleChangePassword = (currentPassword: string, newPassword: string) => {
    changePasswordMutation.mutate({ currentPassword, newPassword });
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isProcessingRequest = acceptRequestMutation.isPending || rejectRequestMutation.isPending;
  const isSubmittingService = createServiceMutation.isPending || updateServiceMutation.isPending;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Provider Dashboard</h1>
              <p className="text-sm text-muted-foreground">
                Welcome back, {user?.first_name} {user?.last_name}
              </p>
            </div>
            <Button variant="outline" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs defaultValue="requests" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="requests" className="flex items-center gap-2">
              <Inbox className="h-4 w-4" />
              Service Requests
            </TabsTrigger>
            <TabsTrigger value="services" className="flex items-center gap-2">
              <Briefcase className="h-4 w-4" />
              My Services
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              Settings
            </TabsTrigger>
          </TabsList>

          {/* Service Requests Tab */}
          <TabsContent value="requests">
            <RequestInbox
              requests={requestsData?.results || []}
              isLoading={isLoadingRequests}
              onAccept={handleAcceptRequest}
              onReject={handleRejectRequest}
              isProcessing={isProcessingRequest}
            />
          </TabsContent>

          {/* My Services Tab */}
          <TabsContent value="services">
            {viewMode === 'list' ? (
              <ServiceManager
                services={servicesData?.results || []}
                isLoading={isLoadingServices}
                onEdit={handleEditService}
                onDelete={handleDeleteService}
                onAdd={handleAddService}
                isDeletingId={deletingServiceId}
              />
            ) : (
              <ServiceForm
                service={selectedService}
                onSubmit={handleSubmitService}
                onCancel={handleCancelForm}
                isSubmitting={isSubmittingService}
              />
            )}
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings">
            <div className="max-w-2xl">
              <PasswordChangeForm
                onSubmit={handleChangePassword}
                isSubmitting={changePasswordMutation.isPending}
              />
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
