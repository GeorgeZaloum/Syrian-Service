import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { LogOut, Search, FileText, AlertCircle, Settings } from 'lucide-react';
import { useAuth, useToast } from '@/hooks';
import { useNavigate } from 'react-router-dom';
import {
  ServiceSearchPanel,
  ServiceGrid,
  ServiceRequestModal,
  RequestList,
  ProblemReportForm,
  RecommendationDisplay,
  ProblemHistory,
  PasswordChangeForm,
} from '@/components/user';
import { servicesApi, requestsApi, problemsApi, authApi } from '@/lib/api';
import type { Service, ServiceSearchParams, InputType, ProblemReport } from '@/types';

export function UserDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [searchParams, setSearchParams] = useState<ServiceSearchParams>({});
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [isRequestModalOpen, setIsRequestModalOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState<ProblemReport | null>(null);

  // Fetch services
  const { data: servicesData, isLoading: isLoadingServices } = useQuery({
    queryKey: ['services', searchParams],
    queryFn: () => servicesApi.list(searchParams),
  });

  // Fetch user's service requests
  const { data: requestsData, isLoading: isLoadingRequests } = useQuery({
    queryKey: ['requests'],
    queryFn: () => requestsApi.list(),
  });

  // Fetch problem reports
  const { data: problemsData, isLoading: isLoadingProblems } = useQuery({
    queryKey: ['problems'],
    queryFn: () => problemsApi.list(),
  });

  // Create service request mutation
  const createRequestMutation = useMutation({
    mutationFn: ({ serviceId, message }: { serviceId: number; message: string }) =>
      requestsApi.create({ service: serviceId, message }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['requests'] });
      toast({
        title: 'Success',
        description: 'Service request sent successfully!',
      });
      setIsRequestModalOpen(false);
      setSelectedService(null);
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to send service request. Please try again.',
        variant: 'destructive',
      });
    },
  });

  // Create problem report mutation
  const createProblemMutation = useMutation({
    mutationFn: ({ inputType, problemText, audioFile }: { inputType: InputType; problemText?: string; audioFile?: File }) =>
      problemsApi.create({ input_type: inputType, problem_text: problemText, audio_file: audioFile }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['problems'] });
      setSelectedReport(data);
      toast({
        title: 'Success',
        description: 'Problem report submitted successfully!',
      });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to submit problem report. Please try again.',
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
        description: error.response?.data?.error?.message || 'Failed to change password. Please check your current password.',
        variant: 'destructive',
      });
    },
  });

  const handleRequestService = (service: Service) => {
    setSelectedService(service);
    setIsRequestModalOpen(true);
  };

  const handleSubmitRequest = (serviceId: number, message: string) => {
    createRequestMutation.mutate({ serviceId, message });
  };

  const handleSubmitProblem = (inputType: InputType, problemText?: string, audioFile?: File) => {
    createProblemMutation.mutate({ inputType, problemText, audioFile });
  };

  const handleChangePassword = (currentPassword: string, newPassword: string) => {
    changePasswordMutation.mutate({ currentPassword, newPassword });
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">User Dashboard</h1>
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
        <Tabs defaultValue="services" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="services" className="flex items-center gap-2">
              <Search className="h-4 w-4" />
              Services
            </TabsTrigger>
            <TabsTrigger value="requests" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              My Requests
            </TabsTrigger>
            <TabsTrigger value="problems" className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              Problem Reports
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              Settings
            </TabsTrigger>
          </TabsList>

          {/* Services Tab */}
          <TabsContent value="services" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <ServiceSearchPanel onSearchChange={setSearchParams} />
              </div>
              <div className="lg:col-span-3">
                <ServiceGrid
                  services={servicesData?.results || []}
                  isLoading={isLoadingServices}
                  onRequestService={handleRequestService}
                />
              </div>
            </div>
          </TabsContent>

          {/* Requests Tab */}
          <TabsContent value="requests">
            <RequestList
              requests={requestsData?.results || []}
              isLoading={isLoadingRequests}
            />
          </TabsContent>

          {/* Problems Tab */}
          <TabsContent value="problems" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-6">
                <ProblemReportForm
                  onSubmit={handleSubmitProblem}
                  isSubmitting={createProblemMutation.isPending}
                />
                <ProblemHistory
                  reports={problemsData?.results || []}
                  isLoading={isLoadingProblems}
                  onSelectReport={setSelectedReport}
                />
              </div>
              <div>
                <RecommendationDisplay
                  report={selectedReport}
                  isLoading={createProblemMutation.isPending}
                />
              </div>
            </div>
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

      {/* Service Request Modal */}
      <ServiceRequestModal
        service={selectedService}
        open={isRequestModalOpen}
        onClose={() => {
          setIsRequestModalOpen(false);
          setSelectedService(null);
        }}
        onSubmit={handleSubmitRequest}
        isSubmitting={createRequestMutation.isPending}
      />
    </div>
  );
}
