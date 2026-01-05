import { useQuery } from '@tanstack/react-query';
import { analyticsApi } from '@/lib/api/analytics';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, UserCheck, Clock, CheckCircle } from 'lucide-react';
import type { AnalyticsFilters } from '@/types';

interface MetricsCardsProps {
  filters?: AnalyticsFilters;
}

export function MetricsCards({ filters }: MetricsCardsProps) {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics', filters],
    queryFn: () => analyticsApi.getDashboardMetrics(filters),
  });

  const metricsData = [
    {
      title: 'Total Users',
      value: metrics?.total_users || 0,
      icon: Users,
      description: 'Registered users',
    },
    {
      title: 'Active Providers',
      value: metrics?.active_providers || 0,
      icon: UserCheck,
      description: 'Approved providers',
    },
    {
      title: 'Pending Requests',
      value: metrics?.pending_requests || 0,
      icon: Clock,
      description: 'Awaiting response',
    },
    {
      title: 'Completed Requests',
      value: metrics?.completed_requests || 0,
      icon: CheckCircle,
      description: 'Successful requests',
    },
  ];

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <CardContent className="p-6">
              <div className="h-20 animate-pulse bg-muted rounded" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metricsData.map((metric) => {
        const Icon = metric.icon;
        return (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">{metric.description}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
