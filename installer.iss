; Inno Setup Script for HL7 Generator 2000
; Requires: Inno Setup 6+
; Input:    dist\hl7gen\  (produced by PyInstaller)
; Output:   installer\HL7Generator2000-Setup.exe

#define MyAppName      "HL7 Generator 2000"
#define MyAppVersion   "1.0.0"
#define MyAppPublisher "Brandon Cunningham"
#define MyAppExeName   "hl7gen.exe"

[Setup]
AppId={{8F3A5E72-C4D1-4B7A-9E6F-1A2B3C4D5E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=HL7Generator2000-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SetupIconFile=
UninstallDisplayName={#MyAppName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Bundle the entire PyInstaller dist folder
Source: "dist\hl7gen\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Include the launcher batch file
Source: "hl7gen.bat"; DestDir: "{app}"; Flags: ignoreversion

; Include .env.example so users have a template
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut to the batch launcher
Name: "{group}\{#MyAppName}"; Filename: "{app}\hl7gen.bat"; WorkingDir: "{app}"; Comment: "Launch HL7 Generator 2000"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\hl7gen.bat"; WorkingDir: "{app}"; Tasks: desktopicon; Comment: "Launch HL7 Generator 2000"

[Run]
; Offer to launch after install
Filename: "{app}\hl7gen.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
// Copy .env.example -> .env if .env doesn't already exist
procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvSrc, EnvDst: String;
begin
  if CurStep = ssPostInstall then
  begin
    EnvSrc := ExpandConstant('{app}\.env.example');
    EnvDst := ExpandConstant('{app}\.env');
    if not FileExists(EnvDst) then
      FileCopy(EnvSrc, EnvDst, False);
  end;
end;
