import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { providersApi, type ProviderApplication } from '@/lib/api/providers';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/hooks/use-toast';
import { CheckCircle, XCircle, Clock } from 'lucide-react';

export function ProviderApplicationList() {
  const [selectedApplication, setSelectedApplication] = useState<ProviderApplication | null>(null);
  const [actionType, setActionType] = useState<'approve' | 'reject' | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['provider-applications'],
    queryFn: providersApi.listApplications,
  });

  const approveMutation = useMutation({
    mutationFn: providersApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-applications'] });
      toast({
        title: 'Application Approved',
        description: 'The provider application has been approved successfully.',
      });
      setSelectedApplication(null);
      setActionType(null);
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to approve the application. Please try again.',
        variant: 'destructive',
      });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: providersApi.reject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['provider-applications'] });
      toast({
        title: 'Application Rejected',
        description: 'The provider application has been rejected.',
      });
      setSelectedApplication(null);
      setActionType(null);
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'Failed to reject the application. Please try again.',
        variant: 'destructive',
      });
    },
  });

  const handleApprove = (application: ProviderApplication) => {
    setSelectedApplication(application);
    setActionType('approve');
  };

  const handleReject = (application: ProviderApplication) => {
    setSelectedApplication(application);
    setActionType('reject');
  };

  const confirmAction = () => {
    if (!selectedApplication) return;

    if (actionType === 'approve') {
      approveMutation.mutate(selectedApplication.id);
    } else if (actionType === 'reject') {
      rejectMutation.mutate(selectedApplication.id);
    }
  };

  const pendingApplications = data?.results.filter(
    (app) => app.approval_status === 'PENDING'
  ) || [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-muted-foreground">Loading applications...</div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        {pendingApplications.length === 0 ? (
          <Card>
            <CardContent className="flex items-center justify-center p-8">
              <div className="text-center">
                <Clock className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No pending applications</p>
              </div>
            </CardContent>
          </Card>
        ) : (
          pendingApplications.map((application) => (
            <Card key={application.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>
                      {application.user_details.first_name} {application.user_details.last_name}
                    </CardTitle>
                    <CardDescription>{application.user_details.email}</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => handleApprove(application)}
                      disabled={approveMutation.isPending || rejectMutation.isPending}
                    >
                      <CheckCircle className="mr-2 h-4 w-4" />
                      Approve
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleReject(application)}
                      disabled={approveMutation.isPending || rejectMutation.isPending}
                    >
                      <XCircle className="mr-2 h-4 w-4" />
                      Reject
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div>
                  <p className="text-sm font-medium mb-2">Service Description:</p>
                  <p className="text-sm text-muted-foreground">{application.service_description}</p>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      <Dialog open={!!selectedApplication && !!actionType} onOpenChange={() => {
        setSelectedApplication(null);
        setActionType(null);
      }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {actionType === 'approve' ? 'Approve Application' : 'Reject Application'}
            </DialogTitle>
            <DialogDescription>
              {actionType === 'approve'
                ? 'Are you sure you want to approve this provider application? The applicant will receive an email notification and gain access to the platform.'
                : 'Are you sure you want to reject this provider application? The applicant will receive an email notification.'}
            </DialogDescription>
          </DialogHeader>
          {selectedApplication && (
            <div className="py-4">
              <p className="text-sm">
                <span className="font-medium">Applicant:</span>{' '}
                {selectedApplication.user_details.first_name} {selectedApplication.user_details.last_name}
              </p>
              <p className="text-sm">
                <span className="font-medium">Email:</span> {selectedApplication.user_details.email}
              </p>
            </div>
          )}
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setSelectedApplication(null);
                setActionType(null);
              }}
            >
              Cancel
            </Button>
            <Button
              variant={actionType === 'approve' ? 'default' : 'destructive'}
              onClick={confirmAction}
              disabled={approveMutation.isPending || rejectMutation.isPending}
            >
              {actionType === 'approve' ? 'Approve' : 'Reject'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
