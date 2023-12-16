import ipaddress

def subnet_division(network_address, subnet_mask, required_subnets):
    # 将输入的网络地址和子网掩码转换为IP网络对象
    network = ipaddress.ip_network(f"{network_address}/{subnet_mask}", strict=False)

    # 计算新子网掩码
    new_prefix_length = network.prefixlen + (required_subnets - 1).bit_length()

    # 生成和打印子网划分方案
    print("子网划分方案：")
    print(f"{'子网地址':<20}{'广播地址':<20}{'可用地址范围':<40}{'子网掩码':<20}")
    for subnet in network.subnets(new_prefix=new_prefix_length):
        network_address_str = str(subnet.network_address)
        broadcast_address_str = str(subnet.broadcast_address)
        range_start_str = str(subnet.network_address + 1)
        range_end_str = str(subnet.broadcast_address - 1)
        subnet_mask_str = str(subnet.with_netmask.split('/')[1])

        print(f"{network_address_str:<20}{broadcast_address_str:<20}"
            f"{range_start_str} - {range_end_str:<40}"
            f"{subnet_mask_str:<20}")


    # 二进制划分方法展示
    print("\n二进制划分方法：")
    bin_network_address = ''.join(f'{octet:08b}' for octet in subnet.network_address.packed)
    bin_subnet_mask = ''.join(f'{octet:08b}' for octet in subnet.netmask.packed)
    print(f"网络地址（二进制）: {bin_network_address}")
    print(f"子网掩码（二进制）: {bin_subnet_mask}")

def main():
    # 用户输入
    network_address = input("请输入网络地址（例如：192.168.1.0）：")
    subnet_mask = input("请输入子网掩码（例如：255.255.255.0）：")
    required_subnets = int(input("请输入所需的网络数："))

    # 执行子网划分
    subnet_division(network_address, subnet_mask, required_subnets)

if __name__ == '__main__':
    main()
