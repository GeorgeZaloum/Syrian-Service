import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { analyticsApi } from '@/lib/api/analytics';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Search, Download } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import type { AnalyticsFilters, ExportParams } from '@/types';

interface SearchAndExportProps {
  filters?: AnalyticsFilters;
}

export function SearchAndExport({ filters }: SearchAndExportProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'users' | 'providers' | 'requests'>('users');
  const [hasSearched, setHasSearched] = useState(false);
  const { toast } = useToast();

  const { data: searchResults, isLoading, refetch } = useQuery({
    queryKey: ['search', searchQuery, searchType],
    queryFn: () => analyticsApi.search(searchQuery, searchType),
    enabled: false,
  });

  const exportMutation = useMutation({
    mutationFn: (params: ExportParams) => analyticsApi.exportData(params),
    onSuccess: (data) => {
      // Create a download link for the CSV file
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${searchType}_export_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast({
        title: 'Export Successful',
        description: 'Your data has been exported to CSV.',
      });
    },
    onError: () => {
      toast({
        title: 'Export Failed',
        description: 'Failed to export data. Please try again.',
        variant: 'destructive',
      });
    },
  });

  const handleSearch = () => {
    if (!searchQuery.trim()) {
      toast({
        title: 'Search Query Required',
        description: 'Please enter a search query.',
        variant: 'destructive',
      });
      return;
    }
    setHasSearched(true);
    refetch();
  };

  const handleExport = () => {
    const exportParams: ExportParams = {
      export_type: searchType,
      ...filters,
    };
    exportMutation.mutate(exportParams);
  };

  const renderTableContent = () => {
    if (!hasSearched) {
      return (
        <TableRow>
          <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
            Enter a search query and click Search to view results
          </TableCell>
        </TableRow>
      );
    }

    if (isLoading) {
      return (
        <TableRow>
          <TableCell colSpan={4} className="text-center py-8">
            Searching...
          </TableCell>
        </TableRow>
      );
    }

    if (!searchResults || searchResults.results.length === 0) {
      return (
        <TableRow>
          <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
            No results found
          </TableCell>
        </TableRow>
      );
    }

    return searchResults.results.map((item: any, index: number) => (
      <TableRow key={index}>
        {searchType === 'users' && (
          <>
            <TableCell>{item.id}</TableCell>
            <TableCell>{item.first_name} {item.last_name}</TableCell>
            <TableCell>{item.email}</TableCell>
            <TableCell>{item.role}</TableCell>
          </>
        )}
        {searchType === 'providers' && (
          <>
            <TableCell>{item.id}</TableCell>
            <TableCell>{item.first_name} {item.last_name}</TableCell>
            <TableCell>{item.email}</TableCell>
            <TableCell>{item.approval_status}</TableCell>
          </>
        )}
        {searchType === 'requests' && (
          <>
            <TableCell>{item.id}</TableCell>
            <TableCell>{item.service_name || 'N/A'}</TableCell>
            <TableCell>{item.requester_name || 'N/A'}</TableCell>
            <TableCell>{item.status}</TableCell>
          </>
        )}
      </TableRow>
    ));
  };

  const getTableHeaders = () => {
    switch (searchType) {
      case 'users':
        return ['ID', 'Name', 'Email', 'Role'];
      case 'providers':
        return ['ID', 'Name', 'Email', 'Status'];
      case 'requests':
        return ['ID', 'Service', 'Requester', 'Status'];
      default:
        return [];
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Search and Export</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search by name, email, or ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <Select value={searchType} onValueChange={(value: any) => setSearchType(value)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="users">Users</SelectItem>
              <SelectItem value="providers">Providers</SelectItem>
              <SelectItem value="requests">Requests</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleSearch} disabled={isLoading}>
            <Search className="mr-2 h-4 w-4" />
            Search
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExport}
            disabled={exportMutation.isPending}
          >
            <Download className="mr-2 h-4 w-4" />
            Export CSV
          </Button>
        </div>

        <div className="border rounded-lg">
          <Table>
            <TableHeader>
              <TableRow>
                {getTableHeaders().map((header) => (
                  <TableHead key={header}>{header}</TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {renderTableContent()}
            </TableBody>
          </Table>
        </div>

        {searchResults && searchResults.results.length > 0 && (
          <div className="text-sm text-muted-foreground">
            Showing {searchResults.results.length} of {searchResults.count} results
          </div>
        )}
      </CardContent>
    </Card>
  );
}
