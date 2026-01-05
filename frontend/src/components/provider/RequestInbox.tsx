import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Clock, CheckCircle, XCircle, User, Calendar } from 'lucide-react';
import type { ServiceRequest, RequestStatus } from '@/types';

interface RequestInboxProps {
  requests: ServiceRequest[];
  isLoading: boolean;
  onAccept: (id: number) => void;
  onReject: (id: number) => void;
  isProcessing: boolean;
}

const statusConfig: Record<
  RequestStatus,
  { label: string; variant: 'default' | 'success' | 'destructive' | 'warning'; icon: React.ReactNode }
> = {
  PENDING: {
    label: 'Pending',
    variant: 'warning',
    icon: <Clock className="h-4 w-4" />,
  },
  ACCEPTED: {
    label: 'Accepted',
    variant: 'success',
    icon: <CheckCircle className="h-4 w-4" />,
  },
  REJECTED: {
    label: 'Rejected',
    variant: 'destructive',
    icon: <XCircle className="h-4 w-4" />,
  },
  COMPLETED: {
    label: 'Completed',
    variant: 'default',
    icon: <CheckCircle className="h-4 w-4" />,
  },
};

interface ConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  confirmText: string;
  isProcessing: boolean;
}

function ConfirmDialog({
  open,
  onClose,
  onConfirm,
  title,
  description,
  confirmText,
  isProcessing,
}: ConfirmDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isProcessing}>
            Cancel
          </Button>
          <Button onClick={onConfirm} disabled={isProcessing}>
            {isProcessing ? 'Processing...' : confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

interface RequestCardProps {
  request: ServiceRequest;
  onAccept: (id: number) => void;
  onReject: (id: number) => void;
  isProcessing: boolean;
}

function RequestCard({ request, onAccept, onReject, isProcessing }: RequestCardProps) {
  const [showAcceptDialog, setShowAcceptDialog] = useState(false);
  const [showRejectDialog, setShowRejectDialog] = useState(false);
  const config = statusConfig[request.status];

  const handleAccept = () => {
    onAccept(request.id);
    setShowAcceptDialog(false);
  };

  const handleReject = () => {
    onReject(request.id);
    setShowRejectDialog(false);
  };

  return (
    <>
      <Card className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h4 className="font-semibold text-lg">Request #{request.id}</h4>
              <Badge variant={config.variant} className="flex items-center gap-1">
                {config.icon}
                {config.label}
              </Badge>
            </div>
            <div className="space-y-1 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span>Requester ID: {request.requester}</span>
              </div>
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <span>{new Date(request.created_at).toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>

        {request.message && (
          <div className="mb-4 p-3 bg-muted rounded-lg">
            <p className="text-sm font-medium mb-1">Message:</p>
            <p className="text-sm text-muted-foreground">{request.message}</p>
          </div>
        )}

        {request.status === 'PENDING' && (
          <div className="flex gap-3">
            <Button
              onClick={() => setShowAcceptDialog(true)}
              disabled={isProcessing}
              className="flex-1"
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Accept
            </Button>
            <Button
              onClick={() => setShowRejectDialog(true)}
              disabled={isProcessing}
              variant="destructive"
              className="flex-1"
            >
              <XCircle className="h-4 w-4 mr-2" />
              Reject
            </Button>
          </div>
        )}

        {request.status !== 'PENDING' && (
          <div className="text-sm text-muted-foreground">
            Updated: {new Date(request.updated_at).toLocaleString()}
          </div>
        )}
      </Card>

      <ConfirmDialog
        open={showAcceptDialog}
        onClose={() => setShowAcceptDialog(false)}
        onConfirm={handleAccept}
        title="Accept Service Request"
        description="Are you sure you want to accept this service request? The requester will be notified."
        confirmText="Accept Request"
        isProcessing={isProcessing}
      />

      <ConfirmDialog
        open={showRejectDialog}
        onClose={() => setShowRejectDialog(false)}
        onConfirm={handleReject}
        title="Reject Service Request"
        description="Are you sure you want to reject this service request? The requester will be notified."
        confirmText="Reject Request"
        isProcessing={isProcessing}
      />
    </>
  );
}

export function RequestInbox({
  requests,
  isLoading,
  onAccept,
  onReject,
  isProcessing,
}: RequestInboxProps) {
  const filterByStatus = (status?: RequestStatus) => {
    if (!status) return requests;
    return requests.filter((req) => req.status === status);
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="p-6 animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (requests.length === 0) {
    return (
      <Card className="p-12 text-center">
        <Clock className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold mb-2">No Service Requests</h3>
        <p className="text-muted-foreground">
          You don't have any service requests yet. They will appear here when users request your services.
        </p>
      </Card>
    );
  }

  const pendingCount = filterByStatus('PENDING').length;
  const acceptedCount = filterByStatus('ACCEPTED').length;
  const rejectedCount = filterByStatus('REJECTED').length;
  const completedCount = filterByStatus('COMPLETED').length;

  return (
    <Tabs defaultValue="all" className="w-full">
      <TabsList className="grid w-full grid-cols-5">
        <TabsTrigger value="all">All ({requests.length})</TabsTrigger>
        <TabsTrigger value="PENDING">Pending ({pendingCount})</TabsTrigger>
        <TabsTrigger value="ACCEPTED">Accepted ({acceptedCount})</TabsTrigger>
        <TabsTrigger value="REJECTED">Rejected ({rejectedCount})</TabsTrigger>
        <TabsTrigger value="COMPLETED">Completed ({completedCount})</TabsTrigger>
      </TabsList>

      <TabsContent value="all" className="space-y-4">
        {requests.map((request) => (
          <RequestCard
            key={request.id}
            request={request}
            onAccept={onAccept}
            onReject={onReject}
            isProcessing={isProcessing}
          />
        ))}
      </TabsContent>

      <TabsContent value="PENDING" className="space-y-4">
        {filterByStatus('PENDING').length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">No pending requests</p>
          </Card>
        ) : (
          filterByStatus('PENDING').map((request) => (
            <RequestCard
              key={request.id}
              request={request}
              onAccept={onAccept}
              onReject={onReject}
              isProcessing={isProcessing}
            />
          ))
        )}
      </TabsContent>

      <TabsContent value="ACCEPTED" className="space-y-4">
        {filterByStatus('ACCEPTED').length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">No accepted requests</p>
          </Card>
        ) : (
          filterByStatus('ACCEPTED').map((request) => (
            <RequestCard
              key={request.id}
              request={request}
              onAccept={onAccept}
              onReject={onReject}
              isProcessing={isProcessing}
            />
          ))
        )}
      </TabsContent>

      <TabsContent value="REJECTED" className="space-y-4">
        {filterByStatus('REJECTED').length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">No rejected requests</p>
          </Card>
        ) : (
          filterByStatus('REJECTED').map((request) => (
            <RequestCard
              key={request.id}
              request={request}
              onAccept={onAccept}
              onReject={onReject}
              isProcessing={isProcessing}
            />
          ))
        )}
      </TabsContent>

      <TabsContent value="COMPLETED" className="space-y-4">
        {filterByStatus('COMPLETED').length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">No completed requests</p>
          </Card>
        ) : (
          filterByStatus('COMPLETED').map((request) => (
            <RequestCard
              key={request.id}
              request={request}
              onAccept={onAccept}
              onReject={onReject}
              isProcessing={isProcessing}
            />
          ))
        )}
      </TabsContent>
    </Tabs>
  );
}
