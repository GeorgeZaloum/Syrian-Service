import { useQuery } from '@tanstack/react-query';
import { analyticsApi } from '@/lib/api/analytics';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { AnalyticsFilters } from '@/types';

interface AnalyticsChartsProps {
  filters?: AnalyticsFilters;
}

export function AnalyticsCharts({ filters }: AnalyticsChartsProps) {
  const { data: userStats, isLoading: loadingUsers } = useQuery({
    queryKey: ['user-statistics', filters],
    queryFn: () => analyticsApi.getUserStatistics(filters),
  });

  const { data: requestStats, isLoading: loadingRequests } = useQuery({
    queryKey: ['request-statistics', filters],
    queryFn: () => analyticsApi.getRequestStatistics(filters),
  });

  const { data: providerStats, isLoading: loadingProviders } = useQuery({
    queryKey: ['provider-statistics', filters],
    queryFn: () => analyticsApi.getProviderStatistics(filters),
  });

  if (loadingUsers || loadingRequests || loadingProviders) {
    return (
      <div className="grid gap-4 md:grid-cols-2">
        {[1, 2, 3].map((i) => (
          <Card key={i}>
            <CardContent className="flex items-center justify-center p-8">
              <div className="text-muted-foreground">Loading chart...</div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {/* User Registration Trends */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>User Registration Trends</CardTitle>
          <CardDescription>New user registrations over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={userStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleDateString()}
                contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="hsl(var(--primary))" 
                strokeWidth={2}
                name="New Users"
                dot={{ fill: 'hsl(var(--primary))' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Service Request Statistics */}
      <Card>
        <CardHeader>
          <CardTitle>Service Requests</CardTitle>
          <CardDescription>Request volume over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={requestStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleDateString()}
                contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }}
              />
              <Legend />
              <Bar 
                dataKey="count" 
                fill="hsl(var(--primary))" 
                name="Requests"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Provider Activity Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Provider Activity</CardTitle>
          <CardDescription>Top providers by request volume</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart 
              data={providerStats?.slice(0, 5).map(p => ({
                ...p,
                provider_name: `${p.first_name} ${p.last_name}`,
                total_requests: p.received_requests_count,
                accepted_requests: p.accepted_requests_count
              }))} 
              layout="vertical"
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis 
                dataKey="provider_name" 
                type="category" 
                width={100}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }}
              />
              <Legend />
              <Bar 
                dataKey="total_requests" 
                fill="hsl(var(--primary))" 
                name="Total Requests"
                radius={[0, 4, 4, 0]}
              />
              <Bar 
                dataKey="accepted_requests" 
                fill="hsl(142.1 76.2% 36.3%)" 
                name="Accepted"
                radius={[0, 4, 4, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
