# cyber-security-botnet

## About
This is a demonstration of a botnet. The system is divided into three parts:
+ **Agent** - agent is a small script (windows or unix), on a zombie computer. Agent in this botnet is infinitely fetching commands to execute from the server. The target architecture was to have as simple agent as possible, so it has no logic. In this way, no updates would be required.
+ **Server** - server is a web service, that a) returns commands to execute to the agents b) manages the botnet - has a little website through which you can add/remove commands, see available agents etc. 
+ **Malware** - the purpose of malware here is to get the agent on as many computers as possible, so it becomes zombied. In this implementation, malware is a mock website, that suggests users to download an antivirus system for your selected operating system. Once you download the installer, it downloads the agent and makes sure it starts within next reboot.

## URLs
+ Malware web (you can open it safely, just don't click on 'download'): http://botnet-agent-injection.surge.sh
+ Admin Panel: http://ec2-35-156-198-4.eu-central-1.compute.amazonaws.com:8080/
