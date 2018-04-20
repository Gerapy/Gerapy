var gerapySelected = []
var cssSelector = null
var xpathSelector = null
var mode = 'single'

$(function () {
    buttons = '<div id="function-buttons"><button class="active" id="single-mode"><i class="fa fa-square-o"></i></button> <button id="multi-mode"><i class="fa fa-clone"></i></button> <button id="detect"><i class="fa fa-magic"></i></button> </div>'
    $(buttons).appendTo($('body'))
})


function reset() {
    gerapySelected.forEach(element => {
        removeStyle(element)
    })
    gerapySelected = []
    cssSelector = xpathSelector = null
}


$(function () {
    $('body').on('click', function (event) {


        isButtons = $(event.target).parents('#function-buttons').length
        console.log(isButtons)
        if (isButtons) {
            return;
        }

        searchIndex = exists(gerapySelected, event.target);

        if (searchIndex >= 0) {
            element = gerapySelected[searchIndex];
            removeStyle(element)
            gerapySelected.splice(searchIndex, 1);
        } else {
            if (mode === 'single') {
                reset();
            }
            addStyle(event.target);
            gerapySelected.push(event.target);
        }

        cssSelector = getCSSSelectorByElement(event.target);
        xpathSelector = xpathGenerator.getElementXPath(event.target);

    })

    $('#single-mode').on('click', function () {
        mode = 'single';
        $('#single-mode').addClass('active');
        $('#multi-mode').removeClass('active');
        $('#mode').text(mode);
        reset();
    });

    $('#multi-mode').on('click', function () {
        mode = 'multi';
        $('#multi-mode').addClass('active');
        $('#single-mode').removeClass('active');
        $('#mode').text(mode);
        reset();
    });


    $('#detect').on('click', function () {
        // set mode
        selectedXPaths = [];
        gerapySelected.forEach((element) => {
            XPath = getXPathByElement(element)
        });
        selectedLength = gerapySelected.length;
        if (selectedLength >= 2) {
            // xpaths
            XPath1 = getXPathByElement(gerapySelected[0]);
            XPath2 = getXPathByElement(gerapySelected[1]);
            commonXPathString = commonSubstring(XPath1, XPath2);
            commonXPath = commonXPathString.replace('[]', '');
            xpathSelector = commonXPath;

            // css
            CSSSelector1 = getCSSSelectorByElement(gerapySelected[0]);
            CSSSelector2 = getCSSSelectorByElement(gerapySelected[1]);
            commonCSSSelectorString = commonSubstring(CSSSelector1, CSSSelector2);
            commonCSSSelector = commonCSSSelectorString.replace(':nth-child()', '');
            cssSelector = commonCSSSelector;
            nodes = getElementsByXPath(commonXPath);
            nodes.forEach((node) => {
                addStyle(node);
                if (!exists(gerapySelected, node)) {
                    gerapySelected.push(node);
                }
            })

        }

        console.log('css-selector', cssSelector);
        console.log('XPath-selector', xpathSelector);

    });
})


