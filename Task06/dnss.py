import dns.resolver

def query_dns(domain, record_type, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    try:
        answer = resolver.resolve(domain, record_type)
        for rdata in answer:
            print(f"{record_type} Record:", rdata.to_text())
            print("Response is", "authoritative" if answer.response.flags & dns.flags.AA else "non-authoritative")
    except Exception as e:
        print(f"Error querying {domain} for {record_type} record: {e}")

if __name__ == "__main__":
    domain_to_query = "www.dhu.edu.cn"
    dns_server_to_use = "114.114.114.114"  # Google's public DNS server
    record_types = ["A", "NS", "SOA", "MX", "CNAME"]

    for record_type in record_types:
        query_dns(domain_to_query, record_type, dns_server_to_use)
