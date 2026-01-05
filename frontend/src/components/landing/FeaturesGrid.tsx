import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { Card } from '@/components/ui/card';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import {
  Search,
  MessageSquare,
  Shield,
  Zap,
  Users,
  BarChart3,
  Brain,
  Clock,
} from 'lucide-react';

interface Feature {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}

const features: Feature[] = [
  {
    icon: <Search className="w-8 h-8" />,
    title: 'Smart Search',
    description: 'Find the perfect service provider with advanced filters for location and cost.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: <MessageSquare className="w-8 h-8" />,
    title: 'Instant Requests',
    description: 'Send service requests directly to providers and get quick responses.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: <Brain className="w-8 h-8" />,
    title: 'AI Recommendations',
    description: 'Get intelligent problem-solving suggestions powered by advanced AI.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: <Shield className="w-8 h-8" />,
    title: 'Verified Providers',
    description: 'All service providers are carefully reviewed and approved by our admin team.',
    color: 'from-orange-500 to-red-500',
  },
  {
    icon: <Clock className="w-8 h-8" />,
    title: 'Real-time Updates',
    description: 'Track your service requests with instant status updates and notifications.',
    color: 'from-indigo-500 to-blue-500',
  },
  {
    icon: <Zap className="w-8 h-8" />,
    title: 'Fast & Efficient',
    description: 'Streamlined workflows ensure quick service delivery and satisfaction.',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: <Users className="w-8 h-8" />,
    title: 'Community Driven',
    description: 'Join thousands of users and providers in our growing marketplace.',
    color: 'from-teal-500 to-cyan-500',
  },
  {
    icon: <BarChart3 className="w-8 h-8" />,
    title: 'Analytics Dashboard',
    description: 'Providers and admins get detailed insights into performance and activity.',
    color: 'from-rose-500 to-pink-500',
  },
];

export const FeaturesGrid = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });
  const prefersReducedMotion = useReducedMotion();

  return (
    <section ref={ref} className="py-20 px-4 bg-white" aria-labelledby="features-heading">
      <div className="container mx-auto max-w-7xl">
        {/* Section Header */}
        <motion.div
          initial={prefersReducedMotion ? { opacity: 1 } : { opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: prefersReducedMotion ? 0 : 0.6 }}
          className="text-center mb-16"
        >
          <h2 id="features-heading" className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Everything You Need
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Powerful features designed to make finding and offering services seamless
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" role="list">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              feature={feature}
              index={index}
              isInView={isInView}
              prefersReducedMotion={prefersReducedMotion}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

interface FeatureCardProps {
  feature: Feature;
  index: number;
  isInView: boolean;
  prefersReducedMotion: boolean;
}

const FeatureCard = ({ feature, index, isInView, prefersReducedMotion }: FeatureCardProps) => {
  return (
    <motion.div
      initial={prefersReducedMotion ? { opacity: 1 } : { opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{
        duration: prefersReducedMotion ? 0 : 0.5,
        delay: prefersReducedMotion ? 0 : index * 0.1,
      }}
      whileHover={prefersReducedMotion ? {} : {
        y: -8,
        transition: { duration: 0.2 },
      }}
      role="listitem"
    >
      <Card className="p-6 h-full border-2 border-gray-100 hover:border-gray-200 hover:shadow-xl transition-all duration-300 group">
        {/* Icon Container */}
        <motion.div
          whileHover={prefersReducedMotion ? {} : { rotate: [0, -10, 10, -10, 0], scale: 1.1 }}
          transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
          className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-white mb-4 group-hover:shadow-lg transition-shadow`}
          aria-hidden="true"
        >
          {feature.icon}
        </motion.div>

        {/* Content */}
        <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
          {feature.title}
        </h3>
        <p className="text-gray-600 leading-relaxed">{feature.description}</p>

        {/* Hover Effect Line */}
        {!prefersReducedMotion && (
          <motion.div
            initial={{ width: 0 }}
            whileHover={{ width: '100%' }}
            transition={{ duration: 0.3 }}
            className={`h-1 bg-gradient-to-r ${feature.color} rounded-full mt-4`}
            aria-hidden="true"
          />
        )}
      </Card>
    </motion.div>
  );
};
