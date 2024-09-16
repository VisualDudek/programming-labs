// changes to 04_tcp.zig:
// - use std.log instead of std.debug.print
// - set log level to default scope

const std = @import("std");
const net = std.net;
const print = std.debug.print;
const posix = std.posix;

pub const std_options = .{
    .log_level = .info,
};

pub fn main() !void {
    const loopback = try net.Ip4Address.parse("127.0.0.1", 5000);
    const localhost = net.Address{ .in = loopback };
    var server = try localhost.listen(.{
        .reuse_port = true,
    });
    defer server.deinit();

    const addr = server.listen_address;
    std.log.info("Listening on {}, access this port to end the program\n", .{addr.getPort()});

    while (true) {
        var client = try server.accept();
        defer client.stream.close();

        std.log.debug("Connection received! {} is sending data.\n", .{client.address});

        var buf: [1024]u8 = undefined;

        // read from the client and echo back
        while (true) {
            const bytesRead = try client.stream.read(&buf);
            if (bytesRead == 0) {
                break;
            }

            var upper: [1024]u8 = undefined;
            var i: usize = 0;
            for (buf) |c| {
                upper[i] = std.ascii.toUpper(c);
                i += 1;
            }

            std.log.debug("{} says {s}\n", .{ client.address, buf[0..bytesRead] });

            _ = try client.stream.write(upper[0..bytesRead]);
        }
    }
}
