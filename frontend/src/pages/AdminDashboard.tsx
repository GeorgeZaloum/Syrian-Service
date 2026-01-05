import { useState } from 'react';
import { MetricsCards } from '@/components/admin/MetricsCards';
import { FilterPanel } from '@/components/admin/FilterPanel';
import { AnalyticsCharts } from '@/components/admin/AnalyticsCharts';
import { ProviderApplicationList } from '@/components/admin/ProviderApplicationList';
import { SearchAndExport } from '@/components/admin/SearchAndExport';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import type { AnalyticsFilters } from '@/types';

export default function AdminDashboard() {
  const [filters, setFilters] = useState<AnalyticsFilters>({});

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <p className="text-muted-foreground">
          Manage provider applications and monitor platform analytics
        </p>
      </div>

      <Tabs defaultValue="analytics" className="space-y-6">
        <TabsList>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="applications">Provider Applications</TabsTrigger>
          <TabsTrigger value="search">Search & Export</TabsTrigger>
        </TabsList>

        <TabsContent value="analytics" className="space-y-6">
          <FilterPanel onFiltersChange={setFilters} />
          <MetricsCards filters={filters} />
          <AnalyticsCharts filters={filters} />
        </TabsContent>

        <TabsContent value="applications" className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Pending Applications</h2>
            <ProviderApplicationList />
          </div>
        </TabsContent>

        <TabsContent value="search" className="space-y-6">
          <SearchAndExport filters={filters} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
