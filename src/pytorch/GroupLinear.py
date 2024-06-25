import torch
from torch import nn

class GroupLinear(nn.Module):
    """
    使用 kernel_size=1 的 Conv1d 实现的分组全连接层。

    使用示例:
    group_linear = GroupLinear(in_channels=256, out_channels=128, groups=8)
    input = torch.randn(4, 739, 256)  # (bs, seq_len, in_channels)
    output = group_linear(input)  # (bs, seq_len, out_channels)
    group_linear_weight = group_linear.weight  # (out_channels, in_channels)
    """

    def __init__(self, in_channels, out_channels, groups):
        super(GroupLinear, self).__init__()
        self.groups = groups
        if in_channels % groups != 0 or out_channels % groups != 0:
            raise ValueError("in_channels and out_channels must be divisible by groups, "
                             "but got in_channels={}, out_channels={}, groups={}"
                             .format(in_channels, out_channels, groups))
        self.in_channels_per_group = in_channels // groups
        self.out_channels_per_group = out_channels // groups
        self.conv = nn.Conv1d(in_channels=in_channels,
                              out_channels=out_channels,
                              kernel_size=1,
                              groups=groups,
                              bias=False)

    @property
    def weight(self):
        return self.conv.weight

    @weight.setter
    def weight(self, value):
        self.conv.weight = value

    @property
    def bias(self):
        return self.conv.bias

    @bias.setter
    def bias(self, value):
        self.conv.bias = value

    def forward(self, x):
        # 要求输入形状为 (bs, seq_len, in_channels)
        x = x.permute(0, 2, 1)  # 转换为 (bs, in_channels, seq_len)
        x = self.conv(x)
        x = x.permute(0, 2, 1)
        x = x.contiguous()
        return x

    def get_fc_weight(self):
        """
        获取等效的全连接形式的权重，一个分块对角矩阵，每个块代表一个分组的权重。
        形状：(out_channels, in_channels)
        """
        full_weight_matrix = torch.zeros((self.conv.out_channels, self.conv.in_channels))
        step_in = self.in_channels_per_group
        step_out = self.out_channels_per_group
        weight = self.weight

        for i in range(self.groups):
            start_row = i * step_out
            end_row = (i + 1) * step_out
            start_col = i * step_in
            end_col = (i + 1) * step_in
            weight_now = weight[start_row:end_row, :, 0]
            full_weight_matrix[start_row:end_row, start_col:end_col] = weight_now

        return full_weight_matrix