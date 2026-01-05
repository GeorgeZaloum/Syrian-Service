import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Lightbulb, Clock } from 'lucide-react';
import type { ProblemReport } from '@/types';

interface RecommendationDisplayProps {
  report: ProblemReport | null;
  isLoading: boolean;
}

export function RecommendationDisplay({ report, isLoading }: RecommendationDisplayProps) {
  if (isLoading) {
    return (
      <Card className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="h-5 w-5 text-primary animate-pulse" />
          <h3 className="text-xl font-semibold">Generating Recommendations...</h3>
        </div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-200 rounded animate-pulse"></div>
          ))}
        </div>
      </Card>
    );
  }

  if (!report) {
    return null;
  }

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-primary" />
          <h3 className="text-xl font-semibold">AI Recommendations</h3>
        </div>
        <Badge variant="outline" className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          {new Date(report.created_at).toLocaleString()}
        </Badge>
      </div>

      <div className="mb-4 p-4 bg-muted rounded-lg">
        <p className="text-sm font-medium mb-1">Your Problem:</p>
        <p className="text-sm text-muted-foreground">{report.problem_text}</p>
      </div>

      <div className="space-y-3">
        <p className="text-sm font-medium">Recommended Solutions:</p>
        {report.recommendations && report.recommendations.length > 0 ? (
          <ol className="space-y-3">
            {report.recommendations.map((recommendation, index) => (
              <li key={index} className="flex gap-3">
                <span className="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-sm font-semibold">
                  {index + 1}
                </span>
                <p className="flex-1 text-sm">{recommendation}</p>
              </li>
            ))}
          </ol>
        ) : (
          <p className="text-sm text-muted-foreground">No recommendations available.</p>
        )}
      </div>
    </Card>
  );
}
