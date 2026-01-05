import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Clock, CheckCircle, XCircle } from 'lucide-react';
import type { ServiceRequest, RequestStatus } from '@/types';

interface RequestListProps {
  requests: ServiceRequest[];
  isLoading: boolean;
}

const statusConfig: Record<RequestStatus, { label: string; variant: 'default' | 'success' | 'destructive' | 'warning'; icon: React.ReactNode }> = {
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

function RequestCard({ request }: { request: ServiceRequest }) {
  const config = statusConfig[request.status];
  
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h4 className="font-semibold">Service Request #{request.id}</h4>
          <p className="text-sm text-muted-foreground mt-1">
            {new Date(request.created_at).toLocaleDateString()}
          </p>
        </div>
        <Badge variant={config.variant} className="flex items-center gap-1">
          {config.icon}
          {config.label}
        </Badge>
      </div>
      {request.message && (
        <p className="text-sm text-muted-foreground mt-2">{request.message}</p>
      )}
    </Card>
  );
}

export function RequestList({ requests, isLoading }: RequestListProps) {
  const filterByStatus = (status?: RequestStatus) => {
    if (!status) return requests;
    return requests.filter((req) => req.status === status);
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="p-4 animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (requests.length === 0) {
    return (
      <Card className="p-12 text-center">
        <p className="text-muted-foreground">No service requests yet.</p>
      </Card>
    );
  }

  return (
    <Tabs defaultValue="all" className="w-full">
      <TabsList className="grid w-full grid-cols-5">
        <TabsTrigger value="all">All</TabsTrigger>
        <TabsTrigger value="PENDING">Pending</TabsTrigger>
        <TabsTrigger value="ACCEPTED">Accepted</TabsTrigger>
        <TabsTrigger value="REJECTED">Rejected</TabsTrigger>
        <TabsTrigger value="COMPLETED">Completed</TabsTrigger>
      </TabsList>

      <TabsContent value="all" className="space-y-4">
        {requests.map((request) => (
          <RequestCard key={request.id} request={request} />
        ))}
      </TabsContent>

      <TabsContent value="PENDING" className="space-y-4">
        {filterByStatus('PENDING').map((request) => (
          <RequestCard key={request.id} request={request} />
        ))}
      </TabsContent>

      <TabsContent value="ACCEPTED" className="space-y-4">
        {filterByStatus('ACCEPTED').map((request) => (
          <RequestCard key={request.id} request={request} />
        ))}
      </TabsContent>

      <TabsContent value="REJECTED" className="space-y-4">
        {filterByStatus('REJECTED').map((request) => (
          <RequestCard key={request.id} request={request} />
        ))}
      </TabsContent>

      <TabsContent value="COMPLETED" className="space-y-4">
        {filterByStatus('COMPLETED').map((request) => (
          <RequestCard key={request.id} request={request} />
        ))}
      </TabsContent>
    </Tabs>
  );
}
