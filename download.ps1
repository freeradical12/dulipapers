$client = new-object System.Net.WebClient
$files = "pubmed23n0001.xml.gz", "pubmed23n0002.xml.gz"
foreach ($file in $files) {
    $url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/" + $file
    $output = "pubmed_data\" + $file
    $client.DownloadFile($url, $output)
}
