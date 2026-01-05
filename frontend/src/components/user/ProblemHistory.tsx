import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { History, MessageSquare, Mic } from 'lucide-react';
import type { ProblemReport } from '@/types';

interface ProblemHistoryProps {
  reports: ProblemReport[];
  isLoading: boolean;
  onSelectReport: (report: ProblemReport) => void;
}

export function ProblemHistory({ reports, isLoading, onSelectReport }: ProblemHistoryProps) {
  if (isLoading) {
    return (
      <Card className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <History className="h-5 w-5" />
          Problem History
        </h3>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded animate-pulse"></div>
          ))}
        </div>
      </Card>
    );
  }

  if (reports.length === 0) {
    return (
      <Card className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <History className="h-5 w-5" />
          Problem History
        </h3>
        <p className="text-muted-foreground text-center py-8">
          No problem reports yet. Submit your first problem to get AI recommendations.
        </p>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <History className="h-5 w-5" />
        Problem History
      </h3>
      <div className="space-y-3">
        {reports.map((report) => (
          <Card
            key={report.id}
            className="p-4 cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => onSelectReport(report)}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                {report.input_type === 'TEXT' ? (
                  <MessageSquare className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Mic className="h-4 w-4 text-muted-foreground" />
                )}
                <Badge variant="outline">{report.input_type}</Badge>
              </div>
              <span className="text-xs text-muted-foreground">
                {new Date(report.created_at).toLocaleDateString()}
              </span>
            </div>
            <p className="text-sm line-clamp-2">{report.problem_text}</p>
            <p className="text-xs text-muted-foreground mt-2">
              {report.recommendations?.length || 0} recommendations
            </p>
          </Card>
        ))}
      </div>
    </Card>
  );
}
