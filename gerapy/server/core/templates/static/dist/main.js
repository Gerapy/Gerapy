var gerapySelected = []
var cssSelector = null
var xpathSelector = null
var mode = 'single'

$(function () {
    buttons = '<div id="function-buttons"><button class="active" id="gerapy-single"><i class="fa fa-square-o"></i></button> <button id="gerapy-multi"><i class="fa fa-clone"></i></button> <button id="gerapy-detect"><i class="fa fa-magic"></i></button> <button id="gerapy-reset"><i class="fa fa-retweet"></i></button> </div>'
    $(buttons).appendTo($('body'))
})


function reset() {
    $('.gerapy-chosen').removeClass('gerapy-chosen')
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

    $('#gerapy-single').on('click', function () {
        mode = 'single';
        $('#gerapy-single').addClass('active');
        $('#gerapy-multi').removeClass('active');
        reset();
    });

    $('#gerapy-multi').on('click', function () {
        mode = 'multi';
        $('#gerapy-multi').addClass('active');
        $('#gerapy-single').removeClass('active');
        reset();
    });


    $('#gerapy-detect').on('click', function () {
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

    $('#gerapy-reset').on('click', function () {
        reset()
    })
})


