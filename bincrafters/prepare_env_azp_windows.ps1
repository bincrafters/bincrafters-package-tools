$delete = $(
  Start-Process -PassThru -NoNewWindow cmd.exe '/c rmdir /S /Q "C:\ProgramData\chocolatey"';
  Start-Process -PassThru -NoNewWindow cmd.exe '/c rmdir /S /Q "C:\Strawberry\"';
  Start-Process -PassThru -NoNewWindow cmd.exe '/c rmdir /S /Q "C:\Program Files (x86)\CMake\bin"';
  Start-Process -PassThru -NoNewWindow cmd.exe '/c rmdir /S /Q "C:\Program Files\CMake\bin"';
  Start-Process -PassThru -NoNewWindow cmd.exe '/c del /S /Q "C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"';
  Start-Process -PassThru -NoNewWindow cmd.exe '/c del /S /Q "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"';
)
$delete | Wait-Process
if ($env:CONAN_VISUAL_VERSIONS -eq 15) {
  New-Item -ItemType SymbolicLink -Path "C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe" `
  -Target (get-command cmake).Path
}
if ($env:CONAN_VISUAL_VERSIONS -eq 16) {
  New-Item -ItemType SymbolicLink -Path "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe" `
  -Target (get-command cmake).Path
}
