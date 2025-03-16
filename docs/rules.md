第一部分pairing：
1.Processor（处理器） 和 Motherboard（主板） 之间的 socket 兼容性，我们需要确保处理器的 socket 类型 能够匹配主板的 socket：
Processor（cpu）处理器 的 socket 值必须匹配 Motherboard主板 的 socket 值，
处理器品牌（Intel/AMD）必须匹配主板品牌（Intel 处理器不能用于 AMD 主板，反之亦然）


2.CPU 需要 Power Supply 提供足够的电力（待定）
（1）每个 CPU 有一个 TDP（最大功耗），表示它在高负载时需要的功率（单位：瓦特 W）。
电源（Power Supply）需要至少满足 CPU 的 TDP 需求，否则系统可能无法稳定运行或发生供电不足的情况。
（2）额外考虑 GPU（显卡）:
GPU 也会消耗电力，所以为了安全，给 GPU 额外留出 10% 的功率裕度，即： 
计算总功耗时，需要在 CPU TDP 的基础上 增加 10% 的 GPU 额外功耗。

3.主板（Motherboard）和内存（RAM）需要匹配，主要依据：
（1）Form Factor（主板的物理尺寸）—— 确保主板支持的内存类型和插槽匹配。
（2）Memory Speed（内存速度）—— 确保主板支持的内存速度范围，避免不兼容或降频运行。