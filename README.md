<div align="center">
  
# _Text Retrieval & Search Engine_ :globe_with_meridians:

A collection of multiple command-line programs that utilize various topics involved with text retrieval and search engines.

## Breakdown :pushpin: 
### -- A01 --
<table>
  <tbody>
    <tr>
      <th>Script</th>
      <th align="center">Description</th>
      <th align="center">Usage</th>
    </tr>
    <tr>
      <td align="center"> <code>webcrawler1.py</code> </td>
      <td align="left"> 
        <ul>
          <li> Downloads content of <code>initialURL</code> </li>
          <li> Writes downloaded content in <code>H.txt</code>, where H is the calculated hash value of <code>initialURL</code>, using <code>hashlib</code></li>
          <li> Extracts all hyperlinks of the downloaded content </li>
          <li> Apennds a line at the end of file <code>crawler1.log</code> that includes <code>&lt;H, URL, Download DateTime, HTTP Response Code&gt;</code> </li>
        </ul>
      </td>
      <td align="center"> 
        <code>python3 webcrawler1.py [options] initialURL</code> 
        <br><br>
        [options]: <br>
        <code>--maxdepth</code>: Maximum number of depths to crawl from initialURL <br><br>
        <code> --rewrite</code>: If value is TRUE and H.txt exists for current URL, it re-extracts and re-writes URL. Default is FALSE. <br><br>
        <code>--verbose</code>: If TRUE, prints &lt;URL, depth&gt;. Default is FALSE.
      </td>
    </tr>
    <tr>
      <td align="center"> <code>webcrawler2.py</code> </td>
      <td align="left"> 
        <ul>
          <li> Downloads content of <code>researcherURL</code> </li>
          <li> Writes downloaded content in <code>H.txt</code>, where H is the calculated hash value of <code>researcherURL</code>, using <code>hashlib</code></li>
          <li> Extracts all information from the pages in a JSON format, and saves it to <code>H.json</code></li> 
          <li> Is able to parse past the limited number of publications by sending a POST request to the URL dynamically</li> 
        </ul>
      </td>
      <td align="center"> 
        <code>python3 webcrawler2.py researcherURL</code>       
      </td>
    </tr>
    <tr>
      <td align="center"> <code>webcrawler3.py</code> </td>
      <td align="left"> 
        <ul>
          <li> Downloads content of <code>initialURL</code> </li>
          <li> Writes downloaded content in <code>H.html</code>, where H is the calculated hash value of <code>initialURL</code>, using <code>hashlib</code></li>
          <li> Replaces all HTML tags with 1, assuming that a HTML tag is <code>&lt;?????&gt;</code>, where <code>?????</code> is a combination of any characters having any length. This is done using REGEX to simplify HTML tags' identification and replacement process </li>
          <li> Replaces tokens (words) with 0 </code> </li>
          <li> $\forall 0 \leq j \leq N-1$ calculates $f(i,j)$ and prints $(i*,j*)$ which is the best combination of $i,j$ that maximizes $f(i,j)$
          <li> Writes the identified main content of downloaded page (which is located between $i*$ and $j*$) in H.txt.</li>
          <li> For all calculated values of $i$, $j$ plot function $f(i,j)$ similar to one of the following plots. The x-axis and y-axis are for $i$ and $j$, respectively. The color of the histogram for 2D or z-axis for 3D represents $f(i,j)$ </li>
        </ul><br>
        $$f(i,j) = \sum_{n=0}^{i - 1}{b_n} + \sum_{n=i}^{j}{(1-b_n)} + \sum_{n=j}^{N-1}{b_n}$$
      </td>
      <td align="center"> 
        <code>python3 webcrawler3.py initialURL</code> 
      </td>
    </tr>
  </tbody>
</table>
  
</div>

## Usage :pencil:

### CLI

#### Example for `A01`
> Enter source directory
```sh
$ cd A01
```

## Installation :hammer:

> Install virtual env :
```
$ pip install pipenv
```

> Set env version :
```
$ pipenv --python 3.10
```

> Activate env :
```
$ pipenv shell 
```

> Install dependencies :
```
$ pipenv install -r requirements.txt
```