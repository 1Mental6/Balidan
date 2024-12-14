
        Set-Location -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location
        Set-ItemProperty . -Name Value -Value Allow
        