/** layuiAdmin.std-v1.4.0 LPPL License By https://www.layui.com/admin/ */
;layui.define(["form", "upload"], function (t) {
    var i = layui.$, e = layui.layer, a = (layui.laytpl, layui.setter, layui.view, layui.admin), n = layui.form,
        s = layui.upload;
    var csrftoken = getCookie('csrf-token')
    i("body");
    n.verify({
        nickname: function (t, i) {
            return new RegExp("^[a-zA-Z0-9_一-龥\\s·]+$").test(t) ? /(^\_)|(\__)|(\_+$)/.test(t) ? "用户名首尾不能出现下划线'_'" : /^\d+\d+\d$/.test(t) ? "用户名不能全为数字" : void 0 : "用户名不能有特殊字符"
        }, pass: [/^[\S]{6,12}$/, "密码必须6到12位，且不能出现空格"], repass: function (t) {
            if (t !== i("#LAY_password").val()) return "两次密码输入不一致"
        }
    }), n.on("submit(set_website)", function (t) {
        return e.msg(JSON.stringify(t.field)), !1
    }), n.on("submit(set_system_email)", function (t) {
        return e.msg(JSON.stringify(t.field)), !1
    }), n.on("submit(setmyinfo)", function (t) {
        const field = t.field;
        let options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(field),
        };
        fetch('/api/v1/dashboard/profiles/base_info', options).then(function (obj) {
            return obj.json()
        }).then(function (result) {
            if (result.code === 0) {
                layui.layer.msg(result.message, {time: 500, icon: 1});
            } else {
                layui.layer.msg(result.message, {time: 500, icon: 2});
            }
        })
        return false;
    });
    var r = i("#LAY_avatarSrc");
    s.render({
        headers: {
            'X-CSRFToken': csrftoken,
        },
        url: "/api/v1/dashboard/upload/image", elem: "#LAY_avatarUpload", done: function (t) {
            // 0 == t.status ? r.val(t.url) : e.msg(t.msg, {icon: 5})
            if (t.code === 0) {
                e.msg(t.message, {time: 500, icon: 1}, function () {
                    r.val(t.location)
                });
            } else {
                e.msg(t.message, {time: 500, icon: 2});
            }
        },
    }), a.events.avartatPreview = function (t) {
        var i = r.val();
        e.photos({photos: {title: "查看头像", data: [{src: i}]}, shade: .01, closeBtn: 1, anim: 5})
    }, n.on("submit(setmypass)", function (t) {
        return e.msg(JSON.stringify(t.field)), !1
    }), t("set", {})
});