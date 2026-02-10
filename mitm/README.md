## MITM Starter Template

This directory is a starter template for the MITM portion of the assignment.

### What you need to implement
- Capture traffic between the web app and database.
- Analyze packets for sensitive data and explain the impact.
- Record your findings.
- Include evidence (pcap files or screenshots) alongside your report.

### Getting started
1. Run your capture workflow from this directory or the repo root.
2. Save artifacts (pcap or screenshots) in this folder.
3. Document everything.

Man-in-the-Middle (MiTM) Vulnerability Analysis
Overview

A Man-in-the-Middle (MiTM) vulnerability occurs when an attacker is able to intercept and observe network traffic between two communicating systems without their knowledge. In this environment, several internal services communicated over the network using unencrypted protocols, allowing sensitive information to be transmitted in plaintext. Because no transport-layer encryption (TLS/SSL) or secure authentication channels were enforced, an attacker positioned on the same network segment was able to capture and inspect packets using traffic-sniffing tools.

Exploited Weakness

The MySQL service running on port 3306 transmitted authentication negotiations and query results without encryption. By capturing the traffic stream, it was possible to observe database queries and returned data directly from the packet capture. Specifically, a query retrieving secrets from the secrets table exposed sensitive fields such as secret_name and secret_value. This resulted in the interception of FLAG{n3tw0rk_tr4ff1c_1s_n0t_s3cur3}, demonstrating that confidential application data was accessible to any attacker capable of monitoring the network.

Attack Methodology

The attacker performed packet capture on the network interface connecting the vulnerable containers and filtered traffic destined for the MySQL port. Using a packet analysis tool, the captured TCP stream was reconstructed to reveal application-layer data, including SQL queries and responses. Because the connection was not encrypted, the captured traffic could be read directly without any additional decryption steps, allowing the attacker to extract sensitive credentials, API tokens, and application secrets.

Impact Assessment

The successful MiTM attack demonstrates several significant security risks:

Exposure of sensitive credentials: Database secrets, API tokens, and authentication information can be captured and reused by attackers.

Unauthorized data access: Intercepted secrets enabled further interaction with internal services, including the retrieval of additional flags and protected resources.

Lateral movement opportunities: Attackers can leverage captured credentials to pivot to other services within the network.

Loss of confidentiality and trust: Any application relying on plaintext communication becomes vulnerable to passive surveillance and active manipulation.

In a real-world environment, such vulnerabilities could result in data breaches, account compromise, financial loss, and regulatory violations. The attack highlights the importance of encrypting all service-to-service communications and implementing network monitoring mechanisms capable of detecting suspicious packet-capture activity.