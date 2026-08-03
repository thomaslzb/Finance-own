param(
    [Parameter(Mandatory = $true)]
    [long]$TargetHandle,
    [Parameter(Mandatory = $true)]
    [int]$MoneyHomeProcessId,
    [int]$X = 10,
    [int]$Y = 10,
    [int]$TimeoutMilliseconds = 5000,
    [int]$SelectPosition = -1,
    [ValidateSet("Left", "Right")]
    [string]$MouseButton = "Left",
    [int[]]$InitializePath = @(),
    [ValidateRange(0, 8)]
    [int]$MaxDepth = 4
)

$ErrorActionPreference = "Stop"

if (-not ("MoneyHomeMenuNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class MoneyHomeMenuNative
{
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct GUITHREADINFO
    {
        public int cbSize;
        public int flags;
        public IntPtr hwndActive;
        public IntPtr hwndFocus;
        public IntPtr hwndCapture;
        public IntPtr hwndMenuOwner;
        public IntPtr hwndMoveSize;
        public IntPtr hwndCaret;
        public RECT rcCaret;
    }

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetClassName(IntPtr hWnd, StringBuilder className, int maxCount);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    [DllImport("user32.dll")]
    public static extern bool GetGUIThreadInfo(uint threadId, ref GUITHREADINFO info);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern IntPtr SendMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern int GetMenuItemCount(IntPtr menu);

    [DllImport("user32.dll")]
    public static extern uint GetMenuItemID(IntPtr menu, int position);

    [DllImport("user32.dll")]
    public static extern IntPtr GetSubMenu(IntPtr menu, int position);

    [DllImport("user32.dll")]
    public static extern uint GetMenuState(IntPtr menu, uint item, uint flags);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetMenuString(
        IntPtr menu,
        uint item,
        StringBuilder text,
        int maxCount,
        uint flags
    );
}
'@
}

$targetProcessId = 0
[void][MoneyHomeMenuNative]::GetWindowThreadProcessId(
    [IntPtr]$TargetHandle,
    [ref]$targetProcessId
)
if ($targetProcessId -ne $MoneyHomeProcessId) {
    throw "TargetHandle $TargetHandle 不属于 MoneyHome8 PID $MoneyHomeProcessId。"
}

function Get-MoneyHomePopupMenu {
    param([int]$ProcessId)

    $windows = [System.Collections.Generic.List[long]]::new()
    [MoneyHomeMenuNative]::EnumWindows(
        {
            param([IntPtr]$handle, [IntPtr]$lParam)

            $windowProcessId = 0
            [void][MoneyHomeMenuNative]::GetWindowThreadProcessId(
                $handle,
                [ref]$windowProcessId
            )
            if (
                $windowProcessId -eq $ProcessId -and
                [MoneyHomeMenuNative]::IsWindowVisible($handle)
            ) {
                $className = [System.Text.StringBuilder]::new(64)
                [void][MoneyHomeMenuNative]::GetClassName(
                    $handle,
                    $className,
                    $className.Capacity
                )
                if ($className.ToString() -eq "#32768") {
                    $windows.Add($handle.ToInt64())
                }
            }
            return $true
        },
        [IntPtr]::Zero
    ) | Out-Null
    $windows | Select-Object -First 1
}

function Get-MenuItems {
    param(
        [IntPtr]$MenuHandle,
        [int]$Depth,
        [int]$DepthLimit
    )

    $items = [System.Collections.Generic.List[object]]::new()
    $itemCount = [MoneyHomeMenuNative]::GetMenuItemCount($MenuHandle)
    for ($index = 0; $index -lt $itemCount; $index++) {
        $text = [System.Text.StringBuilder]::new(512)
        [void][MoneyHomeMenuNative]::GetMenuString(
            $MenuHandle,
            [uint32]$index,
            $text,
            $text.Capacity,
            0x0400
        )
        $submenuHandle = [MoneyHomeMenuNative]::GetSubMenu($MenuHandle, $index)
        $children = @()
        if ($submenuHandle -ne [IntPtr]::Zero -and $Depth -lt $DepthLimit) {
            $children = Get-MenuItems `
                -MenuHandle $submenuHandle `
                -Depth ($Depth + 1) `
                -DepthLimit $DepthLimit
        }
        $items.Add([pscustomobject]@{
            position = $index
            command_id = [MoneyHomeMenuNative]::GetMenuItemID($MenuHandle, $index)
            submenu_handle = $submenuHandle.ToInt64()
            state = [MoneyHomeMenuNative]::GetMenuState(
                $MenuHandle,
                [uint32]$index,
                0x0400
            )
            text = $text.ToString()
            children = $children
        })
    }
    $items
}

$position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
$buttonMessages = if ($MouseButton -eq "Right") {
    @(0x0200, 0x0204, 0x0205)
} else {
    @(0x0200, 0x0201, 0x0202)
}
foreach ($message in $buttonMessages) {
    $wParam = if ($message -eq 0x0201) {
        [IntPtr]1
    } elseif ($message -eq 0x0204) {
        [IntPtr]2
    } else {
        [IntPtr]::Zero
    }
    [void][MoneyHomeMenuNative]::PostMessage(
        [IntPtr]$TargetHandle,
        $message,
        $wParam,
        $position
    )
}

$watch = [System.Diagnostics.Stopwatch]::StartNew()
$popupHandle = 0
while ($watch.ElapsedMilliseconds -lt $TimeoutMilliseconds) {
    $popupHandle = Get-MoneyHomePopupMenu -ProcessId $MoneyHomeProcessId
    if ($popupHandle) {
        break
    }
    Start-Sleep -Milliseconds 100
}
if (-not $popupHandle) {
    throw "未发现 MoneyHome8 弹出菜单。"
}

$popupProcessId = 0
$threadId = [MoneyHomeMenuNative]::GetWindowThreadProcessId(
    [IntPtr]$popupHandle,
    [ref]$popupProcessId
)
$threadInfo = New-Object MoneyHomeMenuNative+GUITHREADINFO
$threadInfo.cbSize = [System.Runtime.InteropServices.Marshal]::SizeOf($threadInfo)
if (-not [MoneyHomeMenuNative]::GetGUIThreadInfo($threadId, [ref]$threadInfo)) {
    throw "无法读取弹出菜单线程信息。"
}

# MN_GETHMENU 用于取得 Delphi 所有者绘制弹出菜单的 HMENU。
$menuHandle = [MoneyHomeMenuNative]::SendMessage(
    [IntPtr]$popupHandle,
    0x01E1,
    [IntPtr]::Zero,
    [IntPtr]::Zero
)
$rootItems = @(Get-MenuItems -MenuHandle $menuHandle -Depth 0 -DepthLimit $MaxDepth)
$activeMenuHandle = $menuHandle
foreach ($pathPosition in $InitializePath) {
    $activeItemCount = [MoneyHomeMenuNative]::GetMenuItemCount($activeMenuHandle)
    if ($pathPosition -lt 0 -or $pathPosition -ge $activeItemCount) {
        throw "动态子菜单路径位置超出范围：$pathPosition / $activeItemCount"
    }

    $submenuHandle = [MoneyHomeMenuNative]::GetSubMenu(
        $activeMenuHandle,
        $pathPosition
    )
    if ($submenuHandle -eq [IntPtr]::Zero) {
        throw "动态子菜单路径位置 $pathPosition 不包含子菜单。"
    }

    # Delphi 会在 WM_INITMENUPOPUP 中动态填充“更多交易活动”等子菜单。
    [void][MoneyHomeMenuNative]::SendMessage(
        $threadInfo.hwndMenuOwner,
        0x0117,
        $submenuHandle,
        [IntPtr]($pathPosition -band 0xffff)
    )
    Start-Sleep -Milliseconds 150
    $activeMenuHandle = $submenuHandle
}

$items = @(Get-MenuItems -MenuHandle $activeMenuHandle -Depth 0 -DepthLimit $MaxDepth)
$itemCount = $items.Count

$selectedCommandId = $null
if ($SelectPosition -ge 0) {
    if ($SelectPosition -ge $items.Count) {
        throw "菜单位置超出范围：$SelectPosition / $($items.Count)"
    }
    $selectedCommandId = $items[$SelectPosition].command_id
    if ($selectedCommandId -eq [uint32]::MaxValue) {
        throw "菜单位置 $SelectPosition 是子菜单或分隔线，不能直接发送命令。"
    }

    # 先关闭菜单，再把 WM_COMMAND 发送给实际菜单 owner。
    [void][MoneyHomeMenuNative]::SendMessage(
        [IntPtr]$popupHandle,
        0x01E6,
        [IntPtr]::Zero,
        [IntPtr]::Zero
    )
    [void][MoneyHomeMenuNative]::PostMessage(
        $threadInfo.hwndMenuOwner,
        0x0111,
        [IntPtr]$selectedCommandId,
        [IntPtr]::Zero
    )
}

[pscustomobject]@{
    target_handle = $TargetHandle
    popup_handle = $popupHandle
    owner_handle = $threadInfo.hwndMenuOwner.ToInt64()
    root_menu_handle = $menuHandle.ToInt64()
    menu_handle = $activeMenuHandle.ToInt64()
    initialized_path = $InitializePath
    root_items = $rootItems
    item_count = $itemCount
    items = $items
    selected_position = if ($SelectPosition -ge 0) { $SelectPosition } else { $null }
    selected_command_id = $selectedCommandId
} | ConvertTo-Json -Depth 12
