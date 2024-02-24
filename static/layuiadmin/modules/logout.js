/** layuiAdmin.std-v1.4.0 LPPL License By https://www.layui.com/admin/ */
;layui.define(function (e) {
    var i = (layui.$, layui.layer, layui.laytpl, layui.setter, layui.view, layui.admin);
    i.events.logout = function () {
        fetch('/api/v1/passport/logout').then(function (obj) {
            return obj.json();
        }).then(function (e) {
            if (e.code === 0) {
                layer.msg(e.message, {icon: 1, time: 500}, () => {
                    location.reload();
                });
            } else if (e.code === 4101) {
                layer.msg(e.message, {icon: 2, time: 500}, () => {
                    location.href = `/login?next=${location.pathname}`;
                });
            } else {
                layer.msg(e.message, {icon: 1, time: 500});
            }
        });
    }, e("logout", {})
});