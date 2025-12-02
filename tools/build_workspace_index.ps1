# Build workspace_index.json: list files, size, sha1, excerpt
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Split-Path -Parent $root)

$excludeNames = @('.git','.github','node_modules','target','__pycache__','.pytest_cache')
$binaryExt = '\.exe$|\.dll$|\.class$|\.jar$|\.png$|\.jpg$|\.jpeg$|\.gif$|\.zip$|\.bin$'

$files = Get-ChildItem -Recurse -File | Where-Object {
    ($excludeNames -notcontains $_.Name) -and
    ($excludeNames -notcontains $_.Directory.Name) -and
    ($_.FullName -notmatch $binaryExt)
}

$index = @()
foreach ($f in $files) {
    try { $hash = (Get-FileHash -Algorithm SHA1 -Path $f.FullName).Hash } catch { $hash = '' }
    try { $content = Get-Content -Raw -ErrorAction Stop -Path $f.FullName } catch { $content = '' }
    if ($null -eq $content) { $content = '' }
    $excerpt = if ($content.Length -gt 400) { $content.Substring(0,400) } else { $content }
    $entry = [PSCustomObject]@{
        path = (Resolve-Path $f.FullName).Path
        rel = $f.FullName.Replace((Get-Location).Path + '\\','')
        size = $f.Length
        sha1 = $hash
        excerpt = $excerpt
    }
    $index += $entry
}

$index | ConvertTo-Json -Depth 6 | Out-File -FilePath workspace_index.json -Encoding UTF8
Write-Host "Created workspace_index.json with" ($index.Count) "entries"
