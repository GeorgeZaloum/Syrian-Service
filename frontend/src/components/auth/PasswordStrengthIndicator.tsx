interface PasswordStrengthIndicatorProps {
  password: string;
}

interface StrengthResult {
  score: number;
  label: string;
  color: string;
  requirements: {
    minLength: boolean;
    hasUpperCase: boolean;
    hasLowerCase: boolean;
    hasNumber: boolean;
    hasSpecialChar: boolean;
  };
}

function calculatePasswordStrength(password: string): StrengthResult {
  const requirements = {
    minLength: password.length >= 8,
    hasUpperCase: /[A-Z]/.test(password),
    hasLowerCase: /[a-z]/.test(password),
    hasNumber: /[0-9]/.test(password),
    hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
  };

  const metRequirements = Object.values(requirements).filter(Boolean).length;
  
  let score = 0;
  let label = 'Weak';
  let color = 'bg-red-500';

  if (metRequirements >= 5) {
    score = 100;
    label = 'Strong';
    color = 'bg-green-500';
  } else if (metRequirements >= 4) {
    score = 75;
    label = 'Good';
    color = 'bg-blue-500';
  } else if (metRequirements >= 3) {
    score = 50;
    label = 'Fair';
    color = 'bg-yellow-500';
  } else if (metRequirements >= 1) {
    score = 25;
    label = 'Weak';
    color = 'bg-orange-500';
  }

  return { score, label, color, requirements };
}

export function PasswordStrengthIndicator({ password }: PasswordStrengthIndicatorProps) {
  if (!password) return null;

  const strength = calculatePasswordStrength(password);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-600">Password Strength:</span>
        <span className={`font-medium ${
          strength.score >= 75 ? 'text-green-600' :
          strength.score >= 50 ? 'text-blue-600' :
          strength.score >= 25 ? 'text-yellow-600' :
          'text-red-600'
        }`}>
          {strength.label}
        </span>
      </div>
      
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full transition-all duration-300 ${strength.color}`}
          style={{ width: `${strength.score}%` }}
        />
      </div>

      <div className="text-xs space-y-1 text-gray-600">
        <div className={strength.requirements.minLength ? 'text-green-600' : ''}>
          {strength.requirements.minLength ? '✓' : '○'} At least 8 characters
        </div>
        <div className={strength.requirements.hasUpperCase ? 'text-green-600' : ''}>
          {strength.requirements.hasUpperCase ? '✓' : '○'} One uppercase letter
        </div>
        <div className={strength.requirements.hasLowerCase ? 'text-green-600' : ''}>
          {strength.requirements.hasLowerCase ? '✓' : '○'} One lowercase letter
        </div>
        <div className={strength.requirements.hasNumber ? 'text-green-600' : ''}>
          {strength.requirements.hasNumber ? '✓' : '○'} One number
        </div>
        <div className={strength.requirements.hasSpecialChar ? 'text-green-600' : ''}>
          {strength.requirements.hasSpecialChar ? '✓' : '○'} One special character
        </div>
      </div>
    </div>
  );
}
