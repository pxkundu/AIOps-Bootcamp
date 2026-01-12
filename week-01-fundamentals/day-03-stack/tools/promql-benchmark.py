#!/usr/bin/env python3
"""
PromQL Query Performance Benchmarking Tool

Compares the performance of different PromQL queries to help you optimize.
"""

import requests
import time
import statistics
from datetime import datetime, timedelta

class PromQLBenchmark:
    def __init__(self, prometheus_url="http://localhost:9090"):
        self.base_url = prometheus_url
        self.results = []

    def benchmark_query(self, query, iterations=10):
        """Run a query multiple times and measure performance."""
        print(f"\n📊 Benchmarking: {query}")
        print("=" * 80)
        
        timings = []
        sample_counts = []
        
        for i in range(iterations):
            start = time.time()
            response = requests.get(
                f"{self.base_url}/api/v1/query",
                params={"query": query}
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                result_type = data.get('data', {}).get('resultType')
                results = data.get('data', {}).get('result', [])
                sample_count = len(results)
                
                timings.append(elapsed)
                sample_counts.append(sample_count)
                
                print(f"  Run {i+1}: {elapsed:.3f}s | {sample_count} series")
            else:
                print(f"  Run {i+1}: ERROR - {response.text}")
                return None
        
        # Calculate statistics
        avg_time = statistics.mean(timings)
        min_time = min(timings)
        max_time = max(timings)
        p95_time = statistics.quantiles(timings, n=20)[18] if len(timings) > 1 else avg_time
        
        avg_samples = statistics.mean(sample_counts)
        
        result = {
            "query": query,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "p95_time": p95_time,
            "avg_samples": avg_samples,
            "iterations": iterations
        }
        
        self.results.append(result)
        
        print(f"\n  📈 Results:")
        print(f"     Average: {avg_time:.3f}s")
        print(f"     Min: {min_time:.3f}s")
        print(f"     Max: {max_time:.3f}s")
        print(f"     P95: {p95_time:.3f}s")
        print(f"     Avg Samples: {avg_samples:.0f}")
        
        # Performance rating
        if avg_time < 0.1:
            rating = "🟢 EXCELLENT"
        elif avg_time < 0.5:
            rating = "🟡 GOOD"
        elif avg_time < 1.0:
            rating = "🟠 ACCEPTABLE"
        else:
            rating = "🔴 SLOW - OPTIMIZE!"
        
        print(f"     Rating: {rating}")
        
        return result

    def compare_queries(self, queries):
        """Compare multiple query variations."""
        print("\n🔬 Comparative Analysis")
        print("=" * 80)
        
        for query in queries:
            self.benchmark_query(query)
        
        # Sort by performance
        sorted_results = sorted(self.results, key=lambda x: x['avg_time'])
        
        print("\n\n🏆 Performance Ranking:")
        print("=" * 80)
        for idx, result in enumerate(sorted_results, 1):
            speedup = sorted_results[-1]['avg_time'] / result['avg_time']
            print(f"{idx}. {result['avg_time']:.3f}s ({speedup:.1f}x faster than slowest)")
            print(f"   Query: {result['query'][:70]}...")
        
        # Best practices report
        print("\n\n💡 Optimization Tips:")
        print("=" * 80)
        
        slowest = sorted_results[-1]
        fastest = sorted_results[0]
        
        if slowest['avg_samples'] > 1000:
            print("⚠️  High cardinality detected!")
            print("   - Consider adding more specific label filters")
            print("   - Use recording rules for frequently-run queries")
        
        if slowest['avg_time'] > 1.0:
            print("⚠️  Query is slow!")
            print("   - Reduce time range if possible")
            print("   - Use rate() instead of irate() for smoother results")
            print("   - Consider aggregating before filtering")
        
        print(f"\n✅ Best performer: {fastest['query'][:50]}...")
        print(f"   Time: {fastest['avg_time']:.3f}s")

def main():
    benchmark = PromQLBenchmark()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          PromQL Query Performance Benchmarking Tool          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Example: Compare different ways to calculate error rate
    print("Example 1: Error Rate Calculation")
    print("-" * 80)
    
    queries = [
        # Method 1: Direct division
        '''sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))''',
        
        # Method 2: With by clause (more granular)
        '''sum by (job) (rate(http_requests_total{status=~"5.."}[5m])) / sum by (job) (rate(http_requests_total[5m]))''',
        
        # Method 3: Using increase instead of rate
        '''sum(increase(http_requests_total{status=~"5.."}[5m])) / sum(increase(http_requests_total[5m]))''',
    ]
    
    benchmark.compare_queries(queries)
    
    # Example 2: Memory queries
    print("\n\nExample 2: Memory Usage Queries")
    print("-" * 80)
    
    benchmark.results = []  # Reset results
    
    memory_queries = [
        # Simple query
        'node_memory_MemAvailable_bytes',
        
        # Calculated percentage
        '(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100',
        
        # With rate (unnecessary for gauge)
        'rate(node_memory_MemAvailable_bytes[5m])',
    ]
    
    benchmark.compare_queries(memory_queries)

if __name__ == "__main__":
    main()
