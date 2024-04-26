import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class UserEngagementAnalyzer:
    def __init__(self, df):
        self.df = df

    def aggregate_engagement_metrics(self, column ,group_by ):
        try:
            grouped = self.df.groupby(group_by)
            # column = {'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)'}
            engagement_metrics = grouped.agg(column).reset_index()
            return engagement_metrics
        except Exception as e:
            print("Error occurred during aggregation:", str(e))
            return None
      

    def normalize_engagement_metrics(self, engagement_metrics):
        try:
            scaler = StandardScaler()
            normalized_metrics = scaler.fit_transform(engagement_metrics)
            return normalized_metrics
        except Exception as e:
            print("Error occurred during normalization:", str(e))
            return None

    def classify_engagement_clusters(self, normalized_metrics, n_clusters=3):
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(normalized_metrics)
            return clusters
        except Exception as e:
            print("Error occurred during clustering:", str(e))
            return None

    def compute_cluster_statistics(self, engagement_metrics, clusters, column):
        try:
            engagement_metrics['cluster'] = clusters
            cluster_statistics = engagement_metrics.groupby('cluster').agg(column)
            return cluster_statistics
        except Exception as e:
            print("Error occurred during cluster statistics computation:", str(e))
            return None


    def visualize_cluster_statistics(self, cluster_statistics):
        try:
            # Extract relevant statistics from the DataFrame
            clusters = cluster_statistics.index
            metrics = cluster_statistics.columns.get_level_values(0)
            values = cluster_statistics.values

            # Create subplots for each engagement metric
            num_metrics = len(metrics)
            fig, axs = plt.subplots(num_metrics, 1, figsize=(10, num_metrics * 5))

            # Plot each engagement metric
            for i, metric in enumerate(metrics):
                ax = axs[i]
                ax.bar(clusters, values[:, i], color='skyblue')
                ax.set_xlabel('Cluster')
                ax.set_ylabel(metric)
                ax.set_title(f'{metric} by Cluster')

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print("An error occurred during visualization:", str(e))

        
    def aggregate_user_traffic_per_application(self, groupBy,top_n=10):
        try:
            app_columns = [col for col in self.df.columns if 'DL' in col or 'UL' in col]
            app_traffic = self.df.groupby(groupBy)[app_columns].sum().sum(axis=1)
            return app_traffic.nlargest(top_n)
        except Exception as e:
            print("Error occurred during application traffic aggregation:", str(e))
            return None

    def plot_top_applications(self,df):
        try:
         
            # Aggregate total data volume for each application
            applications = ['Youtube', 'Netflix', 'Google', 'Email']
            data_volumes = [df['Youtube DL (Bytes)'].sum() + df['Youtube UL (Bytes)'].sum(),
                            df['Netflix DL (Bytes)'].sum() + df['Netflix UL (Bytes)'].sum(),
                            df['Google DL (Bytes)'].sum() + df['Google UL (Bytes)'].sum(),
                            df['Email DL (Bytes)'].sum() + df['Email UL (Bytes)'].sum()]

            # Sort applications by data volume in descending order
            sorted_applications = [app for _, app in sorted(zip(data_volumes, applications), reverse=True)]
            sorted_data_volumes = sorted(data_volumes, reverse=True)

            # Plot the top 3 most used applications
            plt.figure(figsize=(10, 6))
            plt.bar(sorted_applications[:3], sorted_data_volumes[:3])
            plt.xlabel('Application')
            plt.ylabel('Total Data Volume (Bytes)')
            plt.title('Top 3 Most Used Applications by Data Volume')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print("Error occurred during plotting:", str(e))

    def optimize_k(self, normalized_metrics, max_clusters=10):
        try:
            distortions = []
            for k in range(1, max_clusters + 1):
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(normalized_metrics)
                distortions.append(kmeans.inertia_)
            plt.plot(range(1, max_clusters + 1), distortions, marker='o')
            plt.title('Elbow Method for Optimal k')
            plt.xlabel('Number of Clusters')
            plt.ylabel('Distortion')
            plt.show()
        except Exception as e:
            print("Error occurred during elbow method optimization:", str(e))

