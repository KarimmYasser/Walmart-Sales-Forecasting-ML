# Feature engineering utilities for sales forecasting.
# Handles feature group selection and progressive modeling stages.

from Config import FEATURE_GROUPS

# Manages feature selection for different modeling stages.

class FeatureSelector:

    # Initialize with feature groups from config
    def __init__(self):
        self.feature_groups = FEATURE_GROUPS
    
    def get_features_by_stage(self, stage='critical'):
    
        if stage == 'critical':
            return self.feature_groups['critical']
        
        elif stage == 'with_promotion':
            return self.feature_groups['critical'] + self.feature_groups['promotion']
        
        elif stage == 'with_temporal':
            return (self.feature_groups['critical'] + 
                   self.feature_groups['promotion'] + 
                   self.feature_groups['temporal_extended'])
        
        elif stage == 'with_external':
            return (self.feature_groups['critical'] + 
                   self.feature_groups['promotion'] + 
                   self.feature_groups['temporal_extended'] +
                   self.feature_groups['external'])
        
        elif stage == 'full':
            return (self.feature_groups['critical'] + 
                   self.feature_groups['promotion'] + 
                   self.feature_groups['temporal_extended'] +
                   self.feature_groups['external'] +
                   self.feature_groups['advanced'])
        
        else:
            raise ValueError(f"Unknown stage: {stage}")
    
    def get_feature_count(self, stage):
       
        return len(self.get_features_by_stage(stage))
    
    # Print a summary of feature groups and their sizes
    def print_feature_summary(self):
        
        print("\nFeature Groups Summary:")
        print("=" * 60)
        for group, features in self.feature_groups.items():
            print(f"\n{group.upper()}: {len(features)} features")
            print(f"  {', '.join(features[:5])}{'...' if len(features) > 5 else ''}")
