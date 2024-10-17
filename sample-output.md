# Excessive Privileges for Service Account

<div style='margin-top: 30px;'/>

|**Risk**          |High ⚠️⚠️⚠️             |
|:-----------------|:----------------------|
|**Description**   |The service account is granted 'administrators' group privileges, which can lead to privilege escalation if the account is compromised.          |
|**File**          |src/ServiceConfig.ini                 |
|**Reference**     |<details><summary>**None**</summary>Best practice base on trained knowledge. No citation available.</details>            |
|**Line**          |22        |

<div style='margin-top: 50px;'/>

**💡 Recommendation:**

    Limit the service account privileges to the minimum necessary for operation.

**❌ Existing Code:**

```
Groups=administrators
```

**✔️ Recommended Update:**

```
Groups=service_users
```

<br/>

# Disabled Security Features in Test Environment

<div style='margin-top: 30px;'/>|**Risk**          |Medium ⚠️⚠️             |
|:-----------------|:----------------------|
|**Description**   |Security features are disabled in the test environment, which can lead to security vulnerabilities being overlooked.          |
|**File**          |src/ServiceConfig.ini                 |
|**Reference**     |<div data-tooltip='Possibly based on common best practices. No reference found.'>None</div>            |
|**Line**          |7        |

<div style='margin-top: 50px;'/>**💡 Recommendation:**

```
MF:Security$Disabled=false
```

    Ensure security features are enabled even in test environments to catch potential vulnerabilities.
**❌ Existing Code:**

```language=Existing
MF:Security$Disabled=false
```

**✔️ Recommended Update:**

```language=Recommended
MF:Security$Disabled=true
```

<br/>
