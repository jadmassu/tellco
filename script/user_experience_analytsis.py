import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class UserExperienceAnalyzer:
    def __init__(self, df):
        self.df = df

   
    def compute_top_bottom_frequent_values(self, column):
        # Compute top, bottom, and most frequent values
        top_values = self.df[column].nlargest(10)
        bottom_values = self.df[column].nsmallest(10)
        frequent_values = self.df[column].value_counts().nlargest(10)
        return top_values, bottom_values, frequent_values

    def compute_distribution_throughput_per_handset(self):
        # Compute distribution of average throughput per handset type
        distribution = self.df.groupby('Handset Type')['Avg Bearer TP DL (kbps)'].mean()
        return distribution

    def compute_average_tcp_retransmission_per_handset(self):
        # Compute average TCP retransmission per handset type
        average_tcp_retransmission = self.df.groupby('Handset Type')['TCP DL Retrans. Vol (Bytes)'].mean()
        return average_tcp_retransmission

    def perform_kmeans_clustering(self):
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        features = self.df[['TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)']]
        self.df['Cluster'] = kmeans.fit_predict(features)

        # Description of each cluster
        cluster_description = {}
        for cluster_id in range(3):
            cluster_data = self.df[self.df['Cluster'] == cluster_id]
            description = f"Cluster {cluster_id} - Average TCP Retransmission: {cluster_data['TCP DL Retrans. Vol (Bytes)'].mean()}, " \
                          f"Average RTT: {cluster_data['Avg RTT DL (ms)'].mean()}, " \
                          f"Average Throughput: {cluster_data['Avg Bearer TP DL (kbps)'].mean()}"
            cluster_description[cluster_id] = description
        return cluster_description

# Example usage:
# Initialize UserExperienceAnalyzer with your DataFrame
# uea = UserExperienceAnalyzer(df)

# Preprocess the data
# uea.preprocess_data()

# Task 4.1
# aggregated_data = uea.aggregate_network_parameters()

# Task 4.2
# top_tcp, bottom_tcp, frequent_tcp = uea.compute_top_bottom_frequent_values('TCP DL Retrans. Vol (Bytes)')
# top_rtt, bottom_rtt, frequent_rtt = uea.compute_top_bottom_frequent_values('Avg RTT DL (ms)')
# top_throughput, bottom_throughput, frequent_throughput = uea.compute_top_bottom_frequent_values('Avg Bearer TP DL (kbps)')

# Task 4.3
# distribution_throughput_per_handset = uea.compute_distribution_throughput_per_handset()
# average_tcp_retransmission_per_handset = uea.compute_average_tcp_retransmission_per_handset()

# Task 4.4
# cluster_description = uea.perform_kmeans_clustering()
