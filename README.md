Well, today I wanted to download a series of files with Linux,
and the truth is, I couldn't find a download manager that I liked, 
so I said let me do it myself, so I started coding with the help of 
chatGPT and I was able to send it here. Now I really like to change 
its appearance. I'm working hard and I want something in the internet
download manager for Windows, because I feel that Linux lacks something 
like that, I don't know!


خب من امروز خواستم یه سری 
فایل با لینکوس دانلود کنم و حقیقتش یه دانلود منیجر که به دلم بشینه پیدا
نکردم و گفتم بذار خودم اینکارو بکنم و خب شروع کردم به کد زدن با کمک 
chatGPT و تونستم به اینجا برسونمش درحال حاضر خیلی دوست دارم ظاهرشو 
تغییر بدم و دارم روش کار میکنم و دلم میخواد یه چیزی تو مایه های 
internet download manager ویندوز بشه چون احساس میکنم لینکوس یه
همچین چیزی کم داره یا داره من خبر ندارم! 

__________________________________________________________________________________________________
debian:
برای خروجی گرفتن از برنامه PyQt5 و تبدیل آن به یک برنامه قابل اجرا بر روی لینوکس، مراحل زیر را دنبال کنید:

### 1. **ساخت فایل اجرایی با PyInstaller**

[PyInstaller](https://www.pyinstaller.org/) یکی از ابزارهای معروف برای تبدیل برنامه‌های پایتون به فایل‌های اجرایی مستقل است. این ابزار برنامه‌های پایتون را به باینری‌های قابل اجرا (executables) تبدیل می‌کند.

#### نصب PyInstaller:
برای نصب PyInstaller، از pip استفاده کنید:

```bash
pip install pyinstaller
```

#### ساخت فایل اجرایی:
برای ساخت فایل اجرایی از برنامه خود، از دستور زیر استفاده کنید:

```bash
pyinstaller --onefile --windowed Download_Manager.py
```

- `--onefile`: باعث می‌شود که همه چیز در یک فایل اجرایی قرار بگیرد.
- `--windowed`: از باز شدن یک پنجره ترمینال اضافی جلوگیری می‌کند (برای برنامه‌های GUI).

#### پس از اجرای دستور، PyInstaller یک دایرکتوری به نام `dist` ایجاد می‌کند که شامل فایل اجرایی برنامه است.

### 2. **تست و بسته‌بندی**

#### تست فایل اجرایی:
قبل از توزیع، فایل اجرایی را تست کنید تا مطمئن شوید که به درستی کار می‌کند.

#### بسته‌بندی:
برای بسته‌بندی و توزیع برنامه به دیگران، می‌توانید از ابزارهای مختلف استفاده کنید:

- **`AppImage`**: برای ایجاد فایل‌های اجرایی که به راحتی بر روی توزیع‌های مختلف لینوکس نصب و اجرا می‌شوند.
- **`Debian Packages (.deb)`**: برای توزیع برنامه به صورت بسته‌های دبیان که به راحتی نصب می‌شوند.
- **`Flatpak`** و **`Snap`**: برای توزیع و نصب برنامه‌ها به صورت جهانی بر روی توزیع‌های مختلف لینوکس.

### 3. **بسته‌بندی با AppImage**

برای ساخت یک فایل `AppImage`, می‌توانید از ابزار `appimagetool` استفاده کنید:

#### نصب ابزار AppImage:
```bash
sudo apt-get install appimagetool
```

#### ایجاد ساختار دایرکتوری برای AppImage:
ایجاد یک دایرکتوری با ساختار لازم برای AppImage:
```bash
mkdir -p MyApp.AppDir/usr/bin
```

#### کپی فایل اجرایی:
کپی فایل اجرایی PyInstaller به دایرکتوری `bin`:
```bash
cp dist/Download_Manager MyApp.AppDir/usr/bin/
```

#### ایجاد `AppImage`:
ایجاد فایل AppImage با استفاده از `appimagetool`:
```bash
appimagetool MyApp.AppDir
```

### 4. **ساخت بسته Debian (.deb)**

برای ساخت بسته Debian:

#### نصب ابزار dpkg-deb:
```bash
sudo apt-get install dpkg-deb
```

#### ایجاد ساختار دایرکتوری برای بسته:
ایجاد دایرکتوری‌های لازم:
```bash
mkdir -p MyApp/DEBIAN
mkdir -p MyApp/usr/bin
```

#### ایجاد فایل کنترل:
در دایرکتوری `DEBIAN` یک فایل `control` ایجاد کنید که شامل اطلاعات بسته باشد:
```plaintext
Package: download-manager
Version: 1.0
Section: base
Priority: optional
Architecture: all
Depends: python3, python3-pyqt5, python3-requests
Maintainer: Your Name <your.email@example.com>
Description: A simple download manager application
```

#### کپی فایل اجرایی:
کپی فایل اجرایی به دایرکتوری `usr/bin`:
```bash
cp dist/Download_Manager MyApp/usr/bin/
```

#### ساخت بسته:
ساخت بسته Debian با `dpkg-deb`:
```bash
dpkg-deb --build MyApp
```


arch base:

اگر از توزیع Arch Linux استفاده می‌کنید، می‌توانید از ابزارهای مختلفی برای تبدیل برنامه‌های پایتون به فایل‌های اجرایی و بسته‌های قابل نصب استفاده کنید. در اینجا مراحل کلی برای ساخت و بسته‌بندی برنامه پایتون خود برای Arch Linux آورده شده است:

### 1. **ساخت فایل اجرایی با PyInstaller**

ابتدا باید PyInstaller را نصب کنید و با استفاده از آن فایل اجرایی خود را بسازید.

#### نصب PyInstaller:
```bash
pip install pyinstaller
```

#### ساخت فایل اجرایی:
برای تبدیل برنامه پایتون به فایل اجرایی مستقل، از دستور زیر استفاده کنید:

```bash
pyinstaller --onefile --windowed Download_Manager.py
```

این دستور یک فایل اجرایی در دایرکتوری `dist` ایجاد می‌کند.

### 2. **ساخت بسته برای Arch Linux**

برای ساخت بسته‌ها برای Arch Linux، می‌توانید از `makepkg` و `PKGBUILD` استفاده کنید. این ابزارها به شما اجازه می‌دهند تا بسته‌های قابل نصب را برای Arch Linux و توزیع‌های مبتنی بر آن بسازید.

#### ایجاد ساختار دایرکتوری

برای بسته‌بندی برنامه خود، ابتدا باید یک ساختار دایرکتوری مناسب ایجاد کنید:

```bash
mkdir -p MyApp/opt/MyApp
cp dist/Download_Manager MyApp/opt/MyApp/
```

#### ایجاد فایل PKGBUILD

در دایرکتوری اصلی (یعنی همان دایرکتوری که `MyApp` را در آن ایجاد کرده‌اید)، یک فایل به نام `PKGBUILD` ایجاد کنید. این فایل شامل اطلاعاتی است که `makepkg` برای ساخت بسته به آن نیاز دارد. مثال زیر یک فایل `PKGBUILD` ساده است:

```bash
# Maintainer: Your Name <your.email@example.com>
pkgname=download-manager
pkgver=1.0
pkgrel=1
pkgdesc="A simple download manager application"
arch=('x86_64')
url="https://example.com"
license=('GPL')
depends=('python' 'python-pyqt5' 'python-requests')
source=("MyApp.tar.gz")
md5sums=('SKIP')

package() {
    cd "$srcdir/MyApp"
    install -Dm755 opt/MyApp/Download_Manager "$pkgdir/usr/bin/Download_Manager"
}
```

#### بسته‌بندی برنامه

قبل از اجرای `makepkg`, باید `MyApp` را در یک فایل آرشیو tar.gz قرار دهید:

```bash
tar -czf MyApp.tar.gz -C MyApp .
```

سپس از دستور `makepkg` برای ساخت بسته استفاده کنید:

```bash
makepkg -si
```

### 3. **توزیع و نصب**

#### نصب محلی

پس از ساخت بسته، می‌توانید آن را به صورت محلی نصب کنید:

```bash
sudo pacman -U download-manager-1.0-1-x86_64.pkg.tar.zst
```

#### توزیع

برای توزیع بسته، می‌توانید آن را به دیگران ارسال کنید یا در مخازن محلی یا عمومی Arch Linux قرار دهید.

