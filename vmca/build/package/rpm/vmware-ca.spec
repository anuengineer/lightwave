Name:    vmware-ca
Summary: VMware Certificate Authority Service
Version: 6.0.0
Release: 0
Group:   Applications/System
Vendor:  VMware, Inc.
License: VMware
URL:     http://www.vmware.com
BuildArch: x86_64
Requires:  coreutils >= 8.22, openssl >= 1.0.1, krb5 >= 1.12, cyrus-sasl >= 2.1, likewise-open >= 6.2.0, vmware-directory-client >= 6.0, vmware-afd-client >= 6.0, boost >= 1.56
BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1, krb5 >= 1.12, cyrus-sasl >= 2.1, likewise-open-devel >= 6.2.0, vmware-directory-client-devel >= 6.0, vmware-afd-client-devel >= 2.0, sqlite-autoconf, boost >= 1.56

%define _dbdir %_localstatedir/lib/vmware/vmca

%define _likewise_open_bindir %{_likewise_open_prefix}/bin

%define __strip /bin/true

%description
VMware Certificate Authority

%package client
Summary: VMware Certificate Authority Client
Requires:  coreutils >= 8.22, openssl >= 1.0.1, krb5 >= 1.12, cyrus-sasl >= 2.1, likewise-open >= 6.2.0, vmware-directory-client >= 6.0, vmware-afd-client >= 6.0
%description client
Client libraries to communicate with VMware Certificate Authority

%package client-devel
Summary: VMware Certificate Authority Client Development Library
Requires: vmware-ca-client = %{version}
%description client-devel
Development Libraries to communicate with VMware Certificate Authority Service

%build

export CFLAGS="-Wno-pointer-sign -Wno-unused-but-set-variable -Wno-implicit-function-declaration"
cd build
autoreconf -mif .. &&
../configure --prefix=%{_prefix}  \
            --libdir=%{_lib64dir} \
            --localstatedir=/var/lib/vmware/vmca \
            --with-likewise=%{_likewise_open_prefix} \
            --with-vmdir=%{_prefix} \
            --with-afd=%{_prefix} \
            --with-ssl=/usr \
            --with-boost=/usr \
            --enable-debug=yes

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build && make install DESTDIR=%{buildroot}

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    if [ -z "`pidof lwsmd`" ]; then
        /bin/systemctl start lwsmd
    fi

%post

    /sbin/ldconfig

    /bin/mkdir -m 700 -p %{_dbdir}

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade


    case "$1" in
        1)
            %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
            %{_likewise_open_bindir}/lwsm -q refresh
            ;;
        2)
            %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmca.reg
            %{_likewise_open_bindir}/lwsm -q refresh
            ;;
    esac

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            %{_likewise_open_bindir}/lwsm info vmca > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "Stopping the Certificate Authority Service..."
                %{_likewise_open_bindir}/lwsm stop vmca
                echo "Removing service configuration..."
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmca'
                echo "Restarting service control manager..."
                /bin/systemctl restart lwsmd
                sleep 2
                echo "Autostart services..."
                %{_likewise_open_bindir}/lwsm autostart
            fi
            ;;
    esac

%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            /bin/rm -rf %{_dbdir}
            ;;
    esac

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/config/vmca.reg

%files client
%defattr(-,root,root)
%{_bindir}/certool
%{_datadir}/config/certool.cfg
%{_lib64dir}/libvmcaclient.so
%{_lib64dir}/libvmcaclient.so.0
%{_lib64dir}/libvmcaclient.so.0.0.0

%files client-devel
%defattr(-,root,root)
%{_includedir}/vmca.h
%{_includedir}/vmcatypes.h
%{_lib64dir}/libvmcaclient.a
%{_lib64dir}/libvmcaclient.la

%clean

rm -rf $RPM_BUILD_ROOT

# %doc ChangeLog README COPYING

%changelog

