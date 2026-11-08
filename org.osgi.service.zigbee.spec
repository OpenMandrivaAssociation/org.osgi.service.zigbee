Name:		org.osgi.service.zigbee
Version:	1.0.1
Release:	1
Summary:	OSGi ZigBee Device Service API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.zigbee/%{version}/org.osgi.service.zigbee-%{version}-sources.jar
Source1:	https://raw.githubusercontent.com/osgi/osgi/r8-cmpn-final/LICENSE#/org.osgi.service.zigbee-%{version}-LICENSE

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.osgi:osgi.annotation)
BuildRequires:	mvn(org.osgi:org.osgi.util.function)
BuildRequires:	mvn(org.osgi:org.osgi.util.promise)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi ZigBee Device Service 1.0. Nodes, endpoints, ZCL and ZDP frames,
descriptors, and the ZigBee data types. Promise and Predicate are real
return and argument types, so the packaged function 1.2.0 and promise
1.3.0 are compile dependencies. Upstream asked for 1.0.0 of each. The
versioning annotation is provided from osgi.annotation 8.1.0; upstream
asked for 8.0.1. This build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
cp -p %{SOURCE1} LICENSE
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path

root = Path("src/main/java/org/osgi/service/zigbee")
names = sorted(path.name for path in root.glob("*.java"))
expect = [
    "APSException.java",
    "ZCLAttribute.java",
    "ZCLAttributeInfo.java",
    "ZCLCluster.java",
    "ZCLCommandResponse.java",
    "ZCLCommandResponseStream.java",
    "ZCLEventListener.java",
    "ZCLException.java",
    "ZCLFrame.java",
    "ZCLHeader.java",
    "ZCLReadStatusRecord.java",
    "ZDPException.java",
    "ZDPFrame.java",
    "ZDPResponse.java",
    "ZigBeeDataInput.java",
    "ZigBeeDataOutput.java",
    "ZigBeeDataTypes.java",
    "ZigBeeEndpoint.java",
    "ZigBeeEvent.java",
    "ZigBeeException.java",
    "ZigBeeGroup.java",
    "ZigBeeHost.java",
    "ZigBeeLinkQuality.java",
    "ZigBeeNode.java",
    "ZigBeeRoute.java",
    "package-info.java",
]
if names != expect:
    raise SystemExit("java files " + " ".join(names))
desc = sorted(path.name for path in (root / "descriptions").glob("*.java"))
expect_desc = [
    "ZCLAttributeDescription.java",
    "ZCLClusterDescription.java",
    "ZCLCommandDescription.java",
    "ZCLDataTypeDescription.java",
    "ZCLGlobalClusterDescription.java",
    "ZCLParameterDescription.java",
    "ZCLSimpleTypeDescription.java",
    "ZigBeeDeviceDescription.java",
    "ZigBeeDeviceDescriptionSet.java",
    "package-info.java",
]
if desc != expect_desc:
    raise SystemExit("description java files " + " ".join(desc))
descriptors = sorted(path.name for path in (root / "descriptors").glob("*.java"))
expect_descriptors = [
    "ZigBeeComplexDescriptor.java",
    "ZigBeeFrequencyBand.java",
    "ZigBeeMacCapabiliyFlags.java",
    "ZigBeeNodeDescriptor.java",
    "ZigBeePowerDescriptor.java",
    "ZigBeeServerMask.java",
    "ZigBeeSimpleDescriptor.java",
    "package-info.java",
]
if descriptors != expect_descriptors:
    raise SystemExit("descriptor java files " + " ".join(descriptors))
types = sorted(path.name for path in (root / "types").glob("*.java"))
if len(types) != 56 or "package-info.java" not in types:
    raise SystemExit("type java count " + str(len(types)))
if "ZigBeeIEEE_ADDRESS.java" not in types or "ZigBeeUnsignedInteger64.java" not in types:
    raise SystemExit("type java files changed")
for path in (
    root / "package-info.java",
    root / "descriptions" / "package-info.java",
    root / "descriptors" / "package-info.java",
    root / "types" / "package-info.java",
):
    if '@Version("1.0.1")' not in path.read_text(encoding="utf-8"):
        raise SystemExit("package-info version changed " + str(path))
if list(Path(".").rglob("packageinfo")):
    raise SystemExit("unexpected packageinfo")
if "Apache License" not in Path("LICENSE").read_text(encoding="utf-8"):
    raise SystemExit("LICENSE is not the Apache license")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.zigbee</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>org.osgi:org.osgi.service.zigbee</name>
  <description>OSGi ZigBee Device Service.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.util.function</artifactId>
      <version>1.2.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.util.promise</artifactId>
      <version>1.3.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.annotation</artifactId>
      <version>8.1.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.zigbee</artifactId>",
    "<artifactId>org.osgi.util.function</artifactId>",
    "<version>1.2.0</version>",
    "<artifactId>org.osgi.util.promise</artifactId>",
    "<version>1.3.0</version>",
    "<artifactId>osgi.annotation</artifactId>",
    "<version>8.1.0</version>",
    "<scope>provided</scope>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "SNAPSHOT", "<source>", "<target>", "<parent>", "felix", "maven-bundle-plugin", "<version>1.0.0</version>", "<version>8.0.1</version>", "projectbuild.sourceEncoding"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.zigbee-%{version}.jar --describe-module org.osgi.service.zigbee > module-describe.txt
grep -q '^org.osgi.service.zigbee' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.zigbee-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    names = zf.namelist()
classes = [name for name in names if name.endswith(".class")]
if len(classes) != 100:
    raise SystemExit("class count " + str(len(classes)))
if any("$" in name for name in classes):
    raise SystemExit("unexpected inner class")
required = {
    "org/osgi/service/zigbee/package-info.class",
    "org/osgi/service/zigbee/descriptions/package-info.class",
    "org/osgi/service/zigbee/descriptors/package-info.class",
    "org/osgi/service/zigbee/types/package-info.class",
    "org/osgi/service/zigbee/ZigBeeNode.class",
    "org/osgi/service/zigbee/ZCLCommandResponseStream.class",
    "org/osgi/service/zigbee/types/ZigBeeBoolean.class",
    "org/osgi/service/zigbee/descriptors/ZigBeeMacCapabiliyFlags.class",
}
missing = sorted(required - set(names))
if missing:
    raise SystemExit("missing " + " ".join(missing))
if any(name.endswith("packageinfo") for name in names):
    raise SystemExit("unexpected packageinfo")
PY

%files -f .mfiles
%doc LICENSE
