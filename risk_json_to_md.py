"""
This script converts JSON data to Markdown format.
"""

import json
import snakemd

# Function to convert severity to symbols
def severity_to_symbols(severity):
    """Convert severity to symbols"""
    mapping = {
        "low": "Low ⚠️",
        "medium": "Medium ⚠️⚠️",
        "high": "High ⚠️⚠️⚠️",
        "critical": "Critical ⚠️⚠️⚠️⚠️",
    }
    return mapping.get(severity.lower(), severity)

# Convert JSON to Markdown
def json_to_markdown(data):
    """Convert JSON data to Markdown format"""

    doc = snakemd.new_doc()
    no_reference_html = "<div><details><summary>**None**</summary><br/>Risk detected based on trained knowledge. No citation available.</details></div>"

    json_data = json.loads(data)
    for risk in json_data["risks"]:
        severity = severity_to_symbols(risk["severity"])
        description = risk["description"]
        file = risk["file"]
        starting_line = risk["startingLine"]
        reference = risk["citation"] or no_reference_html
        recommendation = risk["recommendation"]
        existing_code = risk["existingCode"]
        updated_code = risk["updatedCode"]

        doc.add_heading(risk["title"], level=1)

        header = ["**Severity**\t", severity]
        rows = [
            ["**Description**", description],
            ["**File**", file],
            ["**Line**", starting_line],
            ["**Reference**", reference]
        ]
        align = [
            snakemd.Table.Align.LEFT,
            snakemd.Table.Align.LEFT
        ]
        doc.add_table(header, rows, align=align)

        doc.add_paragraph("**💡 Recommendation**")
        doc.add_code(recommendation)
        doc.add_paragraph("**❌ Existing Code**")
        doc.add_code(existing_code)
        doc.add_paragraph("**✔️ Recommended Update**")
        doc.add_code(updated_code)
        doc.add_paragraph("<br/>")

    return doc


# Gets an example code-files payload
def get_example_code_files():
    """Gets an example code-files payload"""

    code_files = r"""<documents>
    <document index="1">
    <source>..\Azure-Core-AI-Playground\src\ServiceConfig.ini</source>
    <document_content>
    [Service]
    Disabled=true
    RunAsAccount=PhyNet
    RequiredDataFolders=networkconfigs,RegionalizationSettingsSdp

    ; Test
    ClusterAlias:PublicPilotFish,Environment:NetSec-Test-*,MF:Security$Disabled=false

    ; PPE
    Environment:NetSec-PPE-SN5N$Disabled=true
    ClusterAlias:PublicPilotFish,Environment:NetSec-PPE-*,MF:Security$Disabled=false
    ClusterAlias:PublicPilotFish,Environment:Network-PPE-*,MF:Security$Disabled=false

    ; Public
    Cluster:BY01P,Environment:NetSec-Prod-BY01P,MF:Security$Disabled=false
    Cluster:SJC05P,Environment:NetSec-Prod-SJC05P,MF:Security$Disabled=false

    ; DAS is not used in national clouds or AGCs.

    [Flattener.FileList]
    %DATADIR%/RegionalizationSettingsSdp/*=

    [ServiceAccount]
    Groups=administrators
    Privileges=SeAuditPrivilege
    EnableProfileGeneration=true

    [Firewall_InBound]
    DeviceAuthorizationHttp=TCP/80:APFW\Backend
    DeviceAuthorizationHttps=TCP/443:APFW\Backend

    [UrlAcls]
    ;Name         - Urls
    ;Description  - Urls that need to be acled for.
    ;Value        - The urls that service account would acl for
    Urls=https://+:443/deviceauthorization

    [Certs]
    ;Name         - port numbers
    ;Description  - Cert that need to be binded, note that only appki cert is supported for now.
    ;Value        - The certs that need to be bind to certain port.
    443=appki

    [AutopilotTests]
    ; https://eng.ms/docs/products/autopilot/autopilot/xping/serviceconfigini-options-for-xping
    CloudMetricMonitoringAccount=azaaamdm

    TestConfigurationFiles=DeviceAuthorizationHttpKeepAlive.xml

    ; for BS and DECOMM machine functions which runs services on-demand tests/heartbeats are disabled
    MF:BS$TestConfigurationFiles=
    MF:DECOMM$TestConfigurationFiles=

    [DataSyncRules]
    APGoldNetwork=VE/Autopilot-Autopilot-VE/SDAPGOLD/Network,600

    [Feature]
    DependOn=DsmsSecretsSoft

    [Feature.DependOn.DsmsSecretsSoft]
    Parameter=-secretConfigurationFile SecretsConfiguration.json -secretDeploymentFile SecretsDeployment.ini.flattened.ini -cacheLookup disable
    Environment:NetSec-Test-*$Parameter=-secretConfigurationFile SecretsConfigurationXPME.json -secretDeploymentFile SecretsDeployment.ini.flattened.ini -cacheLookup disable

    </document_content>
    </document>
    </documents>
    """

    return code_files


# Gets and example diff payload
def get_example_diff():
    """Gets an example diff payload"""

    diff = r"""[Service]
Disabled=false
RunAsAccount=System

[ServiceAccount]
Groups=administrators

[JobObjectLimit]
JobMemoryLimit=1073741824
ProcessorRateControlHardCapPercentage=30

[Firewall_Inbound]
MessageBus=TCP/12000,12002:APFW\Internet
MessageBusInstance=TCP/10600-10620:APFW\Internet
SdnGateway=TCP/9000-9003,10001-10002:APFW\Internet
MockHost=TCP/18192:APFW\Internet
MockHostManager=TCP/18193:APFW\Internet
HostGateway=TCP/8570-8573:APFW\Internet
FlowService=UDP/8666:APFW\Internet
V1Gw=TCP/8550-8554:APFW\Internet
MuxProber=UDP/20000:APFW\Internet"""

    return diff
