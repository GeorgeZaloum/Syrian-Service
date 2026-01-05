import { useNavigate, useRouteError } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, Home, RefreshCw } from 'lucide-react';

export const ErrorPage = () => {
  const navigate = useNavigate();
  const error = useRouteError() as Error;

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-red-50 to-orange-50">
      <Card className="max-w-md w-full">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-destructive/10 p-4">
              <AlertTriangle className="h-12 w-12 text-destructive" />
            </div>
          </div>
          <CardTitle className="text-3xl">Oops! Something went wrong</CardTitle>
          <CardDescription className="text-base">
            An unexpected error occurred. We're sorry for the inconvenience.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-muted p-3 rounded-md mb-4">
              <p className="text-sm font-mono text-muted-foreground break-all">
                {error.message || 'Unknown error'}
              </p>
            </div>
          )}
          <p className="text-sm text-muted-foreground text-center">
            Try refreshing the page or return to the home page.
          </p>
        </CardContent>
        <CardFooter className="flex flex-col sm:flex-row gap-2">
          <Button
            variant="outline"
            className="w-full sm:w-auto"
            onClick={handleRefresh}
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Page
          </Button>
          <Button
            className="w-full sm:w-auto"
            onClick={() => navigate('/')}
          >
            <Home className="h-4 w-4 mr-2" />
            Go Home
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};
