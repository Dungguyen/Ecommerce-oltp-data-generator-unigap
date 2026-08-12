$ErrorActionPreference = "Stop"

$container = "ecommerce_postgres"
$user      = "nguyendung"
$db        = "ecommerce_oltp"

$logFolder = "logs"

if (!(Test-Path $logFolder))
{
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

$logFile = Join-Path $logFolder "deploy.log"

"" | Out-File $logFile

############################################################
# Deploy one SQL file
############################################################

function DeploySingleFile($filePath, $type)
{
    if (!(Test-Path $filePath))
    {
        return
    }

    Write-Host ""
    Write-Host "[$type] $(Split-Path $filePath -Leaf)" -ForegroundColor Cyan

    $sql = Get-Content $filePath -Raw

    $output = $sql |
        docker exec -i $container `
        psql `
        -v ON_ERROR_STOP=1 `
        -U $user `
        -d $db 2>&1

    if ($LASTEXITCODE -eq 0)
    {
        Write-Host "SUCCESS" -ForegroundColor Green
        Add-Content $logFile "[SUCCESS] $filePath"
    }
    else
    {
        Write-Host "FAILED" -ForegroundColor Red
        Write-Host $output -ForegroundColor Yellow

        Add-Content $logFile ""
        Add-Content $logFile "[FAILED ] $filePath"
        Add-Content $logFile $output

        throw "Deployment stopped."
    }
}

############################################################
# Deploy entire folder
############################################################

function DeployFolder($folder,$type)
{
    if(!(Test-Path $folder))
    {
        return
    }

    $files = Get-ChildItem $folder -Filter *.sql | Sort-Object Name

    foreach($file in $files)
    {
        DeploySingleFile $file.FullName $type
    }
}

############################################################
# Header
############################################################

Write-Host ""
Write-Host "========================================"
Write-Host "      SQL DEPLOYMENT FRAMEWORK"
Write-Host "========================================"

############################################################
# Check if database has already been initialized
############################################################

$tableExists = docker exec $container `
    psql `
    -U $user `
    -d $db `
    -tAc `
"SELECT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema='public'
      AND table_name='orders'
);"

if ($tableExists.Trim() -eq "t")
{
    Write-Host ""
    Write-Host "Database already initialized." -ForegroundColor Yellow
    Write-Host "Skip create_tables.sql" -ForegroundColor Yellow
}
else
{
    DeploySingleFile "sql/ddl/create_tables.sql" "DDL"
}

############################################################
# Deploy remaining DDL
############################################################

DeploySingleFile "sql/ddl/create_partitions.sql" "DDL"

DeploySingleFile "sql/ddl/indexes.sql" "DDL"

############################################################
# Views
############################################################

DeployFolder "sql/views" "VIEW"

############################################################
# Functions
############################################################

DeployFolder "sql/functions" "FUNCTION"

############################################################
# Procedures
############################################################

DeployFolder "sql/procedures" "PROCEDURE"

############################################################
# Reports
############################################################

DeployFolder "sql/reports" "REPORT"

############################################################
# Finish
############################################################

Write-Host ""
Write-Host "========================================"
Write-Host "DEPLOY COMPLETED"
Write-Host "========================================"