# Google Scholar Spider Documentation

Google Scholar Spider是一个基于Python的工具，根据给定的关键字检索Google Scholar上发表的文章数据。它允许用户将结果保存为CSV文件，绘制结果，并通过年份和引用次数过滤结果。

## Usage

可以通过运行命令行中的`google_scholar_spider`函数并传递任何所需的参数来使用Google Scholar Spider。可用的参数包括：

--**kw** <keyword> (default "machine learning") 要搜索的关键字。

--**nresults** <number of results> (default 50) 要在Google Scholar上搜索的文章数。

--**notsavecsv** 使用此标志以不保存结果到CSV文件的方式打印结果。

--**csvpath** <path> 要保存导出的CSV文件的路径。默认为当前文件夹。

--**sortby** <column> (default "Citations") 按列排序数据。如果要按每年引用次数排序，请使用--sortby "cit/year"。

--**plotresults** 使用此标志以原始排名在x轴上，引用次数在y轴上绘制结果。

--**startyear** <year> 搜索文章的起始年份。

--**endyear** <year> (default current year) 搜索文章的结束年份。

--**debug** 使用此标志启用调试模式。调试模式用于单元测试并将页面存储在网络档案库中。

## Examples

```
python google_scholar_spider.py --kw "deep learning" --nresults 30 --csvpath "./data" --sortby "cit/year" --plotresults 1
```

此命令在Google Scholar上搜索与“deep learning”相关的文章，检索30个结果，将结果保存到“./data”文件夹中的CSV文件中，按每年引用次数排序数据，并绘制结果。

## License

Google Scholar Spider根据MIT许可证发布。